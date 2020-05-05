from django.shortcuts import render
from .models import BriefSummary
from user.models import User
from django.http import JsonResponse


def getUser(userId):
    matchingUsers = User.objects.filter(uuid = userId)
    if not matchingUsers:
        # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
        matchingUsers = User.objects.filter(pk=userId)
        if not matchingUsers:
            return JsonResponse({'success': False, 'message': 'cannot find a user with that userId'})
    return matchingUsers[0]


# Create your views here.
def trackLink(request, userId, short_link):
    """
    count this link click and route the user to the appropriate link
    """
    if request.method == 'GET':
        mUser = getUser(userId)
        updateReportLinkClickIncrement(mUser)
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

def updateReportLinkClickIncrement(user):
    """
    invoked when the user clicks a tracking link.
    We update the brief summary report here.
    """
    matchingSummaryEntry = BriefSummary.objects.filter(user = user)
    if not matchingSummaryEntry:
        message = "updateReportLinkClickIncrement: cannot find any matching user, exiting without doing anything"
        print(message)
        return JsonResponse({'success': False, 'message': message})
    matchingSummaryEntry.numberOfLinksClicked += 1
    matchingSummaryEntry.save()
    print("updateReportLinkClickIncrement: count incremented for brief summary entry: ", str(matchingSummaryEntry))
