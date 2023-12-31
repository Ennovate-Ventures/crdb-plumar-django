# Generated by Django 4.0.4 on 2022-09-27 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0001_initial'),
        ('startups', '0009_alter_zoommeeting_start_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoommeeting',
            name='opportunity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='opportunity.opportunity'),
        ),
        migrations.AlterField(
            model_name='zoommeeting',
            name='schedule_for',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
