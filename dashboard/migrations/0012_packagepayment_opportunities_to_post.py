# Generated by Django 4.0.4 on 2022-09-28 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_remove_packagepayment_posted_opportunity'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagepayment',
            name='opportunities_to_post',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
