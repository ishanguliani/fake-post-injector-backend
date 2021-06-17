from django.db import models
from user.models import User
from link.models import LinkModel

# Create your models here.
class BriefSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    numberOfLinksSeen = models.IntegerField(default=0, null=True)
    numberOfLinksClicked = models.IntegerField(default=0, null=True)
    numberOfFakeLinksSeen = models.IntegerField(default=0, null=True)
    numberOfFakeLinksClicked = models.IntegerField(default=0, null=True)
    numberOfGenuineLinksSeen = models.IntegerField(default=0, null=True)
    numberOfGenuineLinksClicked = models.IntegerField(default=0, null=True)
    mostRecentInteraction = models.DateTimeField(blank=True, auto_now_add=False)

    def __str__(self):
        return "BriefSummary{" + 'user_uuid: ' + str(self.user.uuid) + ', numberOfLinksSeen: ' + str(self.numberOfLinksSeen) + ", numberOfLinksClicked: " + str(self.numberOfLinksClicked) + ", numberOfFakeLinksSeen: " + str(self.numberOfFakeLinksSeen) + ", numberOfFakeLinksClicked: " + str(self.numberOfFakeLinksClicked) + ", numberOfGenuineLinksSeen: " + str(self.numberOfGenuineLinksSeen) + ", numberOfGenuineLinksClicked: " + str(self.numberOfGenuineLinksClicked) + ', mostRecentInteraction: ' + str(self.mostRecentInteraction) + "}"


class DetailedSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    linkModel = models.ForeignKey(LinkModel, on_delete=models.SET_NULL, null=True)
    redirectionLink = models.CharField(max_length=1000, blank=True, default='')
    # only relevant to fake linkModels, empty for all others
    originalLinkThatWasFaked = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return "DetailedSummary{" + 'user_uuid: ' + str(self.user.uuid) + ", redirectionLink: " + str(self.redirectionLink) + ', linkModel{' + str(self.linkModel) + "'" + "}" + " }"