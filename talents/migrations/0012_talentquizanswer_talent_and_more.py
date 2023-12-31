# Generated by Django 4.0.4 on 2022-09-21 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0011_alter_talentquiz_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentquizanswer',
            name='talent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='talents.talent'),
        ),
        migrations.AlterField(
            model_name='talentquizanswer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='talents.quizquestion'),
        ),
    ]
