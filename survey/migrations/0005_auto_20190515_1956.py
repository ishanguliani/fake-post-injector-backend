# Generated by Django 2.2 on 2019-05-16 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20190515_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnew',
            name='question_page',
        ),
        migrations.AddField(
            model_name='questionnew',
            name='question_page',
            field=models.ManyToManyField(to='survey.QuestionPage'),
        ),
    ]
