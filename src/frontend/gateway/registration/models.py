from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    first_name = models.CharField(max_length=127, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=255, null=True, blank=True, default=None)
    email = models.CharField(max_length=255, null=True, blank=True, default=None)

    last_donation_time = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @classmethod
    def get_or_create_anonymous(cls):
        """ gets or creates the anonymous donor that can be used for donations coming in anonymously
        :return `Donor`
        """
        obj, created = cls.objects.get_or_create(first_name='Anonymous', last_name='Annie', email='anon@anonymous.com')
        return obj

    def __str__(self):
        return f'{self.first_name} {self.last_name} // {self.email} ({self.id})'

