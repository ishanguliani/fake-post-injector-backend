from django.db import models

# Create your models here.
class FakeLinkModel(models.Model):
    fake_picture = models.ImageField(upload_to='images/', verbose_name='Fake Picture')
    fake_link_topic = models.CharField(max_length=1000, default='Entertainment', blank=True)
    fake_link_text = models.CharField(max_length=1000, default='', blank=True)
    fake_link_description = models.CharField(max_length=1000, default='', blank=True)
    fake_link = models.CharField(max_length=1000, default='', blank=True)
    fake_link_header = models.CharField(max_length=1000, default='', blank=True, verbose_name='Fake link source website')

