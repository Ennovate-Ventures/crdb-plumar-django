# Generated by Django 4.0.4 on 2022-09-27 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0008_zoommeeting_match_zoommeeting_opportunity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoommeeting',
            name='start_url',
            field=models.URLField(max_length=1028, null=True),
        ),
    ]