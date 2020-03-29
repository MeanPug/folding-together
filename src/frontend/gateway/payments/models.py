from django.db import models


class Donation(models.Model):
    donor = models.ForeignKey('registration.Donor', related_name='donations', on_delete=models.CASCADE)

    charge_token = models.CharField(max_length=255)
    amount_cents = models.IntegerField(default=0, help_text='the USD amount of the donation in cents')
    created_time = models.DateTimeField(auto_now_add=True)
    charged_time = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def formatted_amount(self):
        """ gets the formatted (USD) amount of this donation
        :return `str`
        """
        return '${:0,.0f}'.format(self.amount_cents / 100.0)

    def __str__(self):
        return f'{self.donor.first_name} // {self.amount_cents} ({self.id})'
