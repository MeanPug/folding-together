# Generated by Django 3.0.4 on 2020-03-29 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_donation_new_donation_event_dispatch_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='charge_token',
            new_name='payment_method_id',
        ),
    ]
