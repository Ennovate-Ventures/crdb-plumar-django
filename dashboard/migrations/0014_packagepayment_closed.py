# Generated by Django 4.0.4 on 2022-09-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_packagepayment_auto_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagepayment',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]