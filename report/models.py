from django.db import models
from user.models import User
from link.models import LinkModel

# Create your models here.
class BriefSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    numberOfLinksSeen = models.IntegerField(default=0, null=True)
    numberOfLinksClicked = models.IntegerField(default=0, null=True)

class DetailedSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    linkModel = models.ForeignKey(LinkModel, on_delete=models.SET_NULL, null=True)