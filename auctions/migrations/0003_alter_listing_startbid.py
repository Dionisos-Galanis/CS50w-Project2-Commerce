# Generated by Django 4.0.3 on 2022-03-28 11:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_closedatettime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='startbid',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
