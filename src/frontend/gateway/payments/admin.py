from django.contrib import admin
from payments import models


class DonationAdmin(admin.ModelAdmin):
    fields = ('donor', 'charge_token', 'created_time', 'charged_time', 'amount_cents', 'formatted_amount')
    raw_id_fields = ('donor',)
    readonly_fields = ('created_time', 'formatted_amount',)


admin.site.register(models.Donation, DonationAdmin)
