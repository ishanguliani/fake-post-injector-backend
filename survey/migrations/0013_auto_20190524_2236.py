# Generated by Django 2.2.1 on 2019-05-25 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0012_auto_20190524_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnew',
            name='question_page',
        ),
        migrations.AddField(
            model_name='questionnew',
            name='question_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.QuestionPage'),
        ),
    ]
