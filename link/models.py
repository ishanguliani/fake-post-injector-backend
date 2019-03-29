from django.db import models
from user.models import User

class LinkType(models.Model):
    """
    What type will a link be ?
        1. genuine
        2. fake
        3. modified_genuine
    """
    type = models.CharField(max_length=30, blank = False, default = "genuine")

    def __str__(self):
        return self.type

# Create your models here.
class LinkModel(models.Model):
    link_text = models.CharField(max_length=100, blank=True)
    link_target = models.CharField(max_length=100, blank=True)
    link_type = models.ForeignKey(LinkType, on_delete=models.SET_NULL, null=True)
    post_text = models.CharField(max_length=100, blank=True)
    author_name = models.CharField(max_length=100, blank=True)
    seen_status = models.BooleanField(default=False)
    clicked_status = models.BooleanField(default=False)
    time_to_view = models.TimeField(blank = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.link_text[:25]) + '..' + ' by ' + str(self.user)
