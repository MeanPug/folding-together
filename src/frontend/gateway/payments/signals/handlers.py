from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from django.utils.text import slugify
from payments.signals import donation_charged
from payments.models import Donation
from payments import utils
import boto3
import json
import logging


client = boto3.client('sqs')


@receiver(donation_charged)
def handle_donation_charged(sender, donation, **kwargs):
    """ handler for the donation_charged event """
    message = {
        'type': 'NEW_DONATION',
        'donor': {
            'name': donation.donor.name,
            'id': donation.donor.id
        },
        'donation': {
            'amount': donation.amount_cents_after_processing_fees
        }
    }

    response = client.send_message(
        QueueUrl=settings.AWS['SQS']['DONATION_QUEUE'],
        MessageBody=json.dumps(message)
    )

    logging.debug(f'got response {response} from sqs')

    donation.new_donation_event_dispatch_time = now()
    donation.save()


@receiver(pre_save, sender=Donation)
def set_donation_slug(sender, instance=None, **kwargs):
    if not instance.slug:
        instance.slug = f'{slugify(instance.donor.name)}-{utils.random_string(8).lower()}'
