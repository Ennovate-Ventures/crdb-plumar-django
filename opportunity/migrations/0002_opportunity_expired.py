# Generated by Django 4.0.4 on 2022-09-28 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
