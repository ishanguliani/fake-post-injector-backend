from django.shortcuts import render
from .models import BriefSummary

# Create your views here.
def trackLink(request, userid, short_link):
    """
    count this link click and route the user to the appropriate link
    """
    if request.method == 'GET':
        pass

def updateReportLinkSeenIncrement(user):
    """
    invoked whenever there is an update to the report to
    increment the link seen count for the given user
    """
    existingEntry = BriefSummary.objects.filter(user = user)
    if not existingEntry:
        # no report entry found for this user, lets create a new report entry
        existingEntry = BriefSummary(user = user)
        print("updateReportLinkSeenIncrement: new entry created!")
    else:
        existingEntry = existingEntry[0]
    print("updateReportLinkSeenIncrement: report entry: ", str(existingEntry))
    existingEntry.numberOfLinksSeen += 1
    existingEntry.save()