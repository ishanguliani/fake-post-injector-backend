# Generated by Django 2.2 on 2019-05-12 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='genuine', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LinkModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_text_original', models.CharField(blank=True, max_length=1000)),
                ('link_text_fake', models.CharField(blank=True, max_length=1000)),
                ('link_target_original', models.CharField(blank=True, max_length=1000)),
                ('link_target_fake', models.CharField(blank=True, max_length=1000)),
                ('authored_text_original', models.CharField(blank=True, max_length=1000)),
                ('authored_text_fake', models.CharField(blank=True, max_length=1000)),
                ('author_name', models.CharField(blank=True, max_length=1000)),
                ('is_seen', models.BooleanField(default=False)),
                ('is_clicked', models.BooleanField(default=False)),
                ('time_to_view', models.TimeField(blank=True)),
                ('preview_title', models.CharField(blank=True, default='', max_length=1000)),
                ('preview_description', models.CharField(blank=True, default='', max_length=2000)),
                ('preview_image', models.CharField(blank=True, default='', max_length=1000)),
                ('preview_url', models.CharField(blank=True, default='', max_length=1000)),
                ('link_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='link.LinkType')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
        ),
    ]
