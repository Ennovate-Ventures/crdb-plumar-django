# Generated by Django 4.0.4 on 2022-09-21 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='time_duration',
            field=models.IntegerField(help_text='Quiz Duration in Minutes', null=True),
        ),
    ]
