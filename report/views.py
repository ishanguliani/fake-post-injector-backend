from django.shortcuts import render
from .models import BriefSummary, DetailedSummary
from user.models import User
from django.http import JsonResponse
from configuration.views import createShortLinkUrl
from link.models import LinkModel
from fakeLinkModel.models import FakeLinkModel
from django.views.generic.base import RedirectView


def getUser(userId):
    matchingUsers = User.objects.filter(uuid = userId)
    if not matchingUsers:
        # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
        matchingUsers = User.objects.filter(pk=userId)
        if not matchingUsers:
            return JsonResponse({'success': False, 'message': 'cannot find a user with that userId'})
    return matchingUsers[0]

def trackLink(request, userId, stringHash):
    """
    count this link click and route the user to the appropriate link
    """
    if request.method == 'GET':
        # be sure to increment counters only if a valid link model exists for the string hash
        linkModel = getLinkModelFromUrl(createShortLinkUrl(userId, stringHash))
        if not linkModel:
            return JsonResponse({'success': False, 'message': 'could not find a valid link model matching that request url'})
        print("trackLink: LinkModel found: ", str(linkModel))
        mUser = getUser(userId)
        updateReportForLinkClickIncrement(mUser)
        updateDetailedSummaryReport(mUser, linkModel)
        return redirectToActualLink(request, stringHash, linkModel)

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

def updateReportForLinkClickIncrement(user):
    """
    invoked when the user clicks a tracking link.
    We update the brief summary report here.
    """
    matchingSummaryEntry = BriefSummary.objects.filter(user = user)
    if not matchingSummaryEntry:
        message = "updateReportLinkClickIncrement: cannot find any matching user, exiting without doing anything"
        print(message)
        return JsonResponse({'success': False, 'message': message})
    matchingSummaryEntry = matchingSummaryEntry[0]
    matchingSummaryEntry.numberOfLinksClicked += 1
    matchingSummaryEntry.save()
    print("updateReportLinkClickIncrement: count incremented for brief summary entry: ", str(matchingSummaryEntry))

def getLinkModelFromUrl(requestUrl):
    linkModel = LinkModel.objects.filter(link_target_fake=requestUrl)
    if not linkModel:
        return
    return linkModel[0]


def updateDetailedSummaryReport(mUser, linkModel):
    """
    Here we add a new entry into the detailed report. This is a mapping as follows -
    {
        user : link model
    }
    """
    newEntry = DetailedSummary(user = mUser, linkModel = linkModel)
    newEntry.save()
    print("updateDetailedSummaryReport: added new entry: ")
    pass

def isFakeLink(linkModel):
    value = linkModel.link_type.type == '3'
    print("isFakeLink: ", str(value))
    return value

def redirectToActualLink(request, stringHash, linkModel):
    """
    extract the actual link for the shortened requestUrl from the FakeLinkModel
    and redirect user to the appropriate page
    """
    print("attempting to redirect to link mapped to short link with string hash: ", stringHash)
    if (isFakeLink(linkModel)):
        fakeLink = FakeLinkModel.objects.filter(short_link = stringHash)
        if not fakeLink:
            errorMessage = "redirectToActualLink: no fake link found for requestUrl: " + stringHash
            print(errorMessage)
            return JsonResponse({'success': False, 'message': errorMessage})
        redirectTo = fakeLink[0].fake_link
    else:
        redirectTo = linkModel.link_target_original
    print("redirectToActualLink: ", 'attempting to redirect to fakeLink: ', redirectTo)
    return RedirectView.as_view(url = redirectTo)(request)
