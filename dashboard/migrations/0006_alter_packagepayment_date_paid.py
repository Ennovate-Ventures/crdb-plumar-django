# Generated by Django 4.0.4 on 2022-09-21 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_packagepayment_active_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagepayment',
            name='date_paid',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
