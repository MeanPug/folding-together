# Generated by Django 3.0.4 on 2020-03-31 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20200329_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='slug',
            field=models.CharField(blank=True, default=None, max_length=127, null=True),
        ),
    ]