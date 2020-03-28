from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_donation_time = models.DateTimeField(null=True, blank=True, default=None)

