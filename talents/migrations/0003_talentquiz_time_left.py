# Generated by Django 4.0.4 on 2022-09-21 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0002_quiz_time_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentquiz',
            name='time_left',
            field=models.IntegerField(null=True),
        ),
    ]
