from payments.models import Donation


class DonationDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(DonationDataMixin, self).get_context_data(**kwargs)
        context['donation_count'] = Donation.objects.count()
        return context
