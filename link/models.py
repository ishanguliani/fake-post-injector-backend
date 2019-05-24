from django.db import models
from user.models import User
from django.template.defaultfilters import truncatechars

class LinkType(models.Model):
    """
    What type will a link be ?
        1. genuine
        4. injected
        3. reactions_changed
    """
    type = models.CharField(max_length=30, blank = False, default = "genuine")

    def __str__(self):
        return str(self.id) + ": " + str(self.type)

# Create your models here.
class LinkModel(models.Model):
    link_text_original = models.CharField(max_length=1000, blank=True)
    link_text_fake = models.CharField(max_length=1000, blank=True)
    link_target_original = models.CharField(max_length=1000, blank=True)
    link_target_fake = models.CharField(max_length=1000, blank=True)
    link_image_src_original = models.CharField(max_length=1000, blank=True)
    link_type = models.ForeignKey(LinkType, on_delete=models.SET_NULL, null=True)
    authored_text_original = models.CharField(max_length=1000, blank=True)
    authored_text_fake = models.CharField(max_length=1000, blank=True)
    author_name = models.CharField(max_length=1000, blank=True)
    is_seen = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)
    time_to_view = models.TimeField(blank = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    preview_title = models.CharField(max_length=1000, blank=True, default='')
    preview_description = models.CharField(max_length=2000, blank=True, default='')
    preview_image = models.CharField(max_length=1000, blank=True, default='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Simple_Rectangle_-_Semi-Transparent.svg/1594px-Simple_Rectangle_-_Semi-Transparent.svg.png')
    preview_url = models.CharField(max_length=1000, blank=True, default='')

    @property
    def property_link_target_original(self):
        return truncatechars(self.link_target_original, 50)

    @property
    def property_link_target_fake(self):
        return truncatechars(self.link_target_fake, 100)

    @property
    def property_authored_text_original(self):
        return truncatechars(self.authored_text_original, 100)

    @property
    def property_link_image_src_original(self):
        return truncatechars(self.link_image_src_original, 1000)

    def __str__(self):
        return "LinkModel{ " + str(self.link_text_original[:25]) + '..' + ' by ' + str(self.user.name) + " }"
        # return str(self.link_text_original[:25]) + '..' + ' by ' + str(self.user)
