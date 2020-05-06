from django.shortcuts import render
from .models import BriefSummary, DetailedSummary
from user.models import User
from django.http import JsonResponse
from configuration.views import createShortLink
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

def trackLink(request, userId, short_link):
    """
    count this link click and route the user to the appropriate link
    """
    if request.method == 'GET':
        mUser = getUser(userId)
        updateReportLinkClickIncrement(mUser)
        requestUrl = createShortLink(userId, short_link)
        print("attempting to fetch fake link model for requestUrl: ", requestUrl)
        linkModel = getLinkModelFromUrl(requestUrl)
        if not linkModel:
            return JsonResponse({'success': False, 'message': 'could not find a valid link model matching that request url'})
        print("trackLink: LinkModel found: ", str(linkModel))
        updateDetailedSummaryReport(mUser, linkModel)
        return redirectToActualLink(request, requestUrl)

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

def redirectToActualLink(request, requestUrl):
    """
    extract the actual link for the shortened requestUrl from the FakeLinkModel
    and redirect user to the appropriate page
    """
    print("attempting to redirect to link mapped to short link: ", requestUrl)
    fakeLink = FakeLinkModel.objects.filter(short_link = requestUrl)
    if not fakeLink:
        errorMessage = "redirectToActualLink: no fake link found for requestUrl: " + requestUrl
        print(errorMessage)
        return JsonResponse({'success': False, 'message': errorMessage})
    fakeLink = fakeLink[0]
    print("redirectToActualLink: ", 'attempting to redirect to fakeLink: ', fakeLink.fake_link )
    return RedirectView.as_view(url = fakeLink.fake_link)(request)