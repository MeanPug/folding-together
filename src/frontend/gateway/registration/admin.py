from django.contrib import admin
from registration import models


class DonorAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'last_donation_time')


admin.site.register(models.Donor, DonorAdmin)
