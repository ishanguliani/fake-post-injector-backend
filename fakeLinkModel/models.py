from django.db import models
from configuration.views import convertLongLinkToShortLink
# Create your models here.
class FakeLinkModel(models.Model):
    fake_picture = models.ImageField(upload_to='images/', verbose_name='Fake Picture')
    fake_link_topic = models.CharField(max_length=1000, default='Entertainment', blank=True)
    fake_link_text = models.CharField(max_length=1000, default='', blank=True)
    fake_link_description = models.CharField(max_length=1000, default='', blank=True)
    fake_link = models.CharField(max_length=1000, default='', blank=True)
    fake_link_header = models.CharField(max_length=1000, default='', blank=True, verbose_name='Fake link source website')
    short_link = models.CharField(max_length=1000, default='', blank=True)

    def __init__(self, fake_picture, fake_link_topic, fake_link_text, fake_link_description, fake_link,
                 fake_link_header, short_link, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake_picture = fake_picture
        self.fake_link_topic = fake_link_topic
        self.fake_link_text = fake_link_text
        self.fake_link_description = fake_link_description
        self.fake_link = fake_link
        self.fake_link_header = fake_link_header
        self.short_link = "https://seng-research.com/track/" + convertLongLinkToShortLink(self.fake_link)

    def __str__(self):
        return "FakeLinkModel{" + 'fake_link_topic' + str(self.fake_link_topic) + 'fake_link_text' + str(self.fake_link_text)[:20] + \
               'fake_link_description' + str(self.fake_link_description)[:20] + 'fake_link' + str(self.fake_link) + 'fake_link_header' + str(self.fake_link_header)[:25] + \
                'short_link' + str(self.short_link) + "}"

