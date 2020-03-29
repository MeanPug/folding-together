from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.http.response import JsonResponse
from django.utils.timezone import now
from payments.forms import DonationForm
from payments.models import Donation
from payments import utils
from registration.models import Donor
import json
import logging

logger = logging.getLogger(__name__)


class DonateView(TemplateView):
    template_name = 'donate.html'

    def post(self, request, *args, **kwargs):
        dat = json.loads(request.body)

        form = DonationForm(data=dat)
        if form.is_valid():
            # if the form has first name, last name, or email, we don't need an anonymous donor
            first_name, last_name, email = [form.cleaned_data.get(k) for k in ('first_name', 'last_name', 'email')]
            if first_name or last_name or email:
                donor = Donor.objects.create(first_name=first_name, last_name=last_name, email=email, last_donation_time=now())
            else:
                donor = Donor.get_or_create_anonymous()

            donation = Donation.objects.create(
                donor=donor,
                charge_token=form.cleaned_data['token'],
                amount_cents=form.cleaned_data['donation_amount_cents']
            )

            charge_success = donation.charge()

            return JsonResponse({'status': 'success', 'redirect': reverse("donation_received")})
        else:
            return JsonResponse({'status': 'error', 'message': json.dumps(form.errors)})


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
