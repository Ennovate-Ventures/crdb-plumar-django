# Generated by Django 4.0.4 on 2022-09-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0010_alter_talentquizanswer_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentquiz',
            name='answers',
            field=models.ManyToManyField(to='talents.quizquestionanswer'),
        ),
    ]
