# Generated by Django 4.0.4 on 2022-09-28 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0003_alter_opportunity_date_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='matched',
            field=models.IntegerField(default=0, max_length=255),
        ),
    ]
