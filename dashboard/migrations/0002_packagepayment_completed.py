# Generated by Django 4.0.4 on 2022-09-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagepayment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
