from django.db import models


class ParentLink(models.Model):
    parent_link = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return "parentLink{" + self.parent_link + "}"

# Create your models here.
class LinkPreviewModel(models.Model):
    parent_link = models.ForeignKey(ParentLink, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, default='', blank=True)
    description = models.CharField(max_length=1000, default='', blank=True)
    image = models.CharField(max_length=1000, default='', blank=True)
    url = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return "LinkPreviewModel{" + self.title + ", " + self.description + ", " + self.image + ", " + self.url + "}"