from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.http.response import JsonResponse
from django.utils.timezone import now
from payments.forms import DonationForm
from payments.models import Donation
from payments import utils
from registration.models import Donor
import stripe
import json
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE['SECRET_KEY']


class DonateView(TemplateView):
    template_name = 'donate.html'

    def post(self, request, *args, **kwargs):
        dat = json.loads(request.body)

        form = DonationForm(data=dat)
        if form.is_valid():
            try:
                # a payment_method_id is only set in the beginning of the stripe payment ceremony
                if 'payment_method_id' in dat:
                    intent = stripe.PaymentIntent.create(
                        payment_method=form.cleaned_data['payment_method_id'],
                        amount=form.cleaned_data['donation_amount_cents'],
                        currency='usd',
                        confirmation_method='manual',
                        confirm=True,
                    )

                    # if the form has first name, last name, or email, we don't need an anonymous donor
                    first_name, last_name, email = [form.cleaned_data.get(k) for k in
                                                    ('first_name', 'last_name', 'email')]
                    if first_name or last_name or email:
                        donor = Donor.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                     last_donation_time=now())
                    else:
                        donor = Donor.get_or_create_anonymous()

                    donation = Donation.objects.create(
                        donor=donor,
                        amount_cents=form.cleaned_data['donation_amount_cents'],
                        payment_method_id=form.cleaned_data['payment_method_id']
                    )
                elif 'payment_intent_id' in dat:
                    intent = stripe.PaymentIntent.confirm(form.cleaned_data['payment_intent_id'])
                    donation = Donation.objects.get(id=form.cleaned_data['donation_id'])
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Form missing required payment information'
                    })
            except stripe.error.CardError as e:
                return JsonResponse({
                    'status': 'error',
                    'message': e.user_message
                })

            return self.handle_payment_intent(intent, donation)

        return JsonResponse({
            'status': 'error',
            'message': json.dumps(form.errors)
        })

    def handle_payment_intent(self, intent, donation):
        if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
            # Tell the client to handle the action
            return JsonResponse({
                'status': 'requires_action',
                'payment_intent_client_secret': intent.client_secret,
                'donation_id': donation.id
            })
        elif intent.status == 'succeeded':
            # The payment didn’t need any additional actions and completed!
            charge_success = donation.finalize_charge()
            return JsonResponse({
                'status': 'success',
                'redirect': reverse("donation_received")
            })
        else:
            # Invalid status
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid PaymentIntent status'
            })


class DonationReceivedView(TemplateView):
    template_name = 'donation_received.html'


class RecentDonationsView(View):
    def get(self, request, *args, **kwargs):
        count = int(request.GET.get('n', 10))

        donations = Donation.objects.select_related('donor').order_by('-id')[:count]

        return JsonResponse({
            'data': [{
                'name': d.donor.first_name,
                'time_canonical': utils.pretty_date(d.created_time),
                'amount': d.formatted_amount
            } for d in donations]
        })
