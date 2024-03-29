from datetime import datetime
from django.shortcuts import render
from .models import BriefSummary, DetailedSummary
from user.models import User
from django.http import JsonResponse
from configuration.views import createShortLinkUrl, convertLongLinkToShortLink
from link.models import LinkModel
from fakeLinkModel.models import FakeLinkModel
from django.views.generic.base import RedirectView
from urllib.parse import urljoin


def getUser(userId):
    matchingUsers = User.objects.filter(uuid=userId)
    if not matchingUsers:
        # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
        matchingUsers = User.objects.filter(pk=userId)
        if not matchingUsers:
            return JsonResponse({'success': False, 'message': 'cannot find a user with that userId'})
    print('getUser(): from userId: ', str(userId),
          ' got user: ', str(matchingUsers[0]))
    return matchingUsers[0]


def registerLinkClick(linkModel):
    """
    mark the link click status and the time on this link model
    """
    linkModel.is_clicked_event_from_ground_data = True
    linkModel.is_clicked_event_from_ground_data_time = datetime.now()
    linkModel.save()
    print("registerLinkClick: link model update: is_clicked_event_from_ground_data" + str(linkModel.is_clicked_event_from_ground_data),
          ", is_clicked_event_from_ground_data_time: ", str(linkModel.is_clicked_event_from_ground_data_time))


def trackLink(request, userId, stringHash):
    """
    count this link click and route the user to the appropriate link
    """
    if request.method == 'GET':
        # be sure to increment counters only if a valid link model exists for the string hash
        fullUrl = createShortLinkUrl(userId, stringHash)
        linkModel = getLinkModelFromUrl(fullUrl)
        if not linkModel:
            return JsonResponse({'success': False, 'message': 'could not find a valid link model matching that request url'})
        registerLinkClick(linkModel)
        mUser = getUser(userId)
        updateReportForLinkClickIncrement(mUser, linkModel)
        updateDetailedSummaryReport(mUser, linkModel, stringHash, fullUrl)
        return redirectToActualLink(request, stringHash, linkModel, fullUrl)


def updateReportLinkSeenIncrement(user, link_type):
    """
    invoked whenever there is an update to the report to
    increment the link seen count for the given user
    """
    existingEntry = BriefSummary.objects.filter(user=user)
    if not existingEntry:
        # no report entry found for this user, lets create a new report entry
        existingEntry = BriefSummary(user=user)
        print("updateReportLinkSeenIncrement: new entry created!")
    else:
        existingEntry = existingEntry[0]
    print("updateReportLinkSeenIncrement: report entry: ", str(existingEntry))
    # if the linkModel linkType is genuine, then update the genuine link
    # counters on this BriefSummary report else update the fake(cloned) link counters only
    if isFakeLinkType(link_type):
        existingEntry.numberOfFakeLinksSeen += 1
    else:
        existingEntry.numberOfGenuineLinksSeen += 1
    # update the common seen counter regardless
    existingEntry.numberOfLinksSeen += 1
    updateMostRecentInteractionTime(existingEntry)
    existingEntry.save()


def updateMostRecentInteractionTime(briefSummaryModel):
    briefSummaryModel.mostRecentInteraction = datetime.now()


def updateReportForLinkClickIncrement(user, linkModel):
    """
    invoked when the user clicks a tracking link.
    We update the brief summary report here.
    """
    matchingSummaryEntry = BriefSummary.objects.filter(user=user)
    if not matchingSummaryEntry:
        message = "updateReportLinkClickIncrement: cannot find any matching user, exiting without doing anything"
        print(message)
        return JsonResponse({'success': False, 'message': message})
    matchingSummaryEntry = matchingSummaryEntry[0]
    # if the linkModel linkType is genuine, then update the genuine link
    # counters on this BriefSummary report else update the fake(cloned) link counters only
    if isFakeLink(linkModel):
        matchingSummaryEntry.numberOfFakeLinksClicked += 1
    else:
        matchingSummaryEntry.numberOfGenuineLinksClicked += 1
    # update the common click counter regardless
    matchingSummaryEntry.numberOfLinksClicked += 1
    updateMostRecentInteractionTime(matchingSummaryEntry)
    matchingSummaryEntry.save()
    print("updateReportLinkClickIncrement: count incremented for brief summary entry: ", str(
        matchingSummaryEntry))


def getLinkModelFromUrl(requestUrl):
    linkModel = LinkModel.objects.filter(link_target_fake=requestUrl)
    if not linkModel:
        return
    return linkModel[0]


def updateDetailedSummaryReport(mUser, linkModel, stringHash, fullUrl=''):
    """
    Here we add a new entry into the detailed report. This is a mapping as follows -
    {
        user : link model
    }
    """
    redirectTo = getRedirectionLink(stringHash, linkModel, fullUrl)
    newEntry = DetailedSummary(user=mUser, redirectionLink=redirectTo,
                               linkModel=linkModel, originalLinkThatWasFaked=linkModel.link_target_original)
    newEntry.save()
    print("updateDetailedSummaryReport: added new entry: ", str(newEntry))


def isFakeLink(linkModel):
    value = linkModel.link_type.id == 3
    print("isFakeLink: ", str(value))
    return value


def isFakeLinkType(link_type):
    value = link_type == 3
    print("isFakeLinkType: ", str(value))
    return value


def getRedirectionLink(stringHash, linkModel, fullUrl=''):
    if (isFakeLink(linkModel)):
        fakeLink = FakeLinkModel.objects.filter(string_hash=stringHash)
        if not fakeLink:
            # also try to fetch by fullUrl
            fakeLink = FakeLinkModel.objects.filter(string_hash=fullUrl)
            if not fakeLink:
                errorMessage = "redirectToActualLink: no fake link found for requestUrl: " + stringHash
                print(errorMessage)
                return JsonResponse({'success': False, 'message': errorMessage})
        redirectTo = fakeLink[0].fake_link
    else:
        redirectTo = linkModel.link_target_original
    return redirectTo


def redirectToActualLink(request, stringHash, linkModel, fullUrl=''):
    """
    extract the actual link for the shortened requestUrl from the FakeLinkModel
    and redirect user to the appropriate page
    """
    print("attempting to redirect to link mapped to short link with string hash: ", stringHash)
    redirectTo = getRedirectionLink(stringHash, linkModel, fullUrl)
    redirectTo = urljoin('http://', redirectTo)
    print("redirectToActualLink: ",
          'attempting to redirect to fakeLink: ', redirectTo)
    return RedirectView.as_view(url=redirectTo)(request)
