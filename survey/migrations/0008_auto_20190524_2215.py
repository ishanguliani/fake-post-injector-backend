# Generated by Django 2.2.1 on 2019-05-25 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_choicenew_is_selected'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choicenew',
            options={'verbose_name': 'Choice', 'verbose_name_plural': 'Choices'},
        ),
        migrations.AlterModelOptions(
            name='questionnew',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questionpage',
            options={'verbose_name': 'Question Page', 'verbose_name_plural': 'Question Pages'},
        ),
        migrations.AlterModelOptions(
            name='questiontype',
            options={'verbose_name': 'Question Type', 'verbose_name_plural': 'Question Types'},
        ),
    ]
