# Generated by Django 2.2 on 2019-05-16 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20190515_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnew',
            name='question_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.QuestionPage'),
        ),
    ]
