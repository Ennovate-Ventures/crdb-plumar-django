# Generated by Django 4.0.4 on 2022-09-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_packagepayment_amount_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagepayment',
            name='can_post',
            field=models.BooleanField(default=True),
        ),
    ]