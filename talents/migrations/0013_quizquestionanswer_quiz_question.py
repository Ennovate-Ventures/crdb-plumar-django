# Generated by Django 4.0.4 on 2022-09-21 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0012_talentquizanswer_talent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestionanswer',
            name='quiz_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='talents.quizquestion'),
        ),
    ]
