# Generated by Django 3.0.3 on 2020-04-17 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FakeLinkModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fake_picture', models.ImageField(upload_to='images/', verbose_name='Fake Picture')),
                ('fake_link_topic', models.CharField(blank=True, default='Entertainment', max_length=1000)),
                ('fake_link_text', models.CharField(blank=True, default='', max_length=1000)),
                ('fake_link_description', models.CharField(blank=True, default='', max_length=1000)),
                ('fake_link', models.CharField(blank=True, default='', max_length=1000)),
                ('fake_link_header', models.CharField(blank=True, default='', max_length=1000, verbose_name='Fake link source website')),
                ('short_link', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
    ]
