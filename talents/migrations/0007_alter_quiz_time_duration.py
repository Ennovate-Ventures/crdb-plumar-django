# Generated by Django 4.0.4 on 2022-09-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0006_talentquiz_timed_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='time_duration',
            field=models.FloatField(help_text='Quiz Duration in Minutes', null=True),
        ),
    ]