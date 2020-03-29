from django import forms


class DonationForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    # donation amount (in US dollars)
    donation_amount = forms.IntegerField(required=True)

    payment_method_id = forms.CharField(required=False)
    payment_intent_id = forms.CharField(required=False)
    # only set on the payment ceremonies requiring card authorization
    donation_id = forms.CharField(required=False)

    def clean_donation_amount(self):
        amount = self.cleaned_data['donation_amount']

        if amount < 1:
            raise forms.ValidationError('please send a donation greater than or equal to $1')

        self.cleaned_data['donation_amount_cents'] = int(amount * 100)

        return amount
