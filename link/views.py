from django.shortcuts import render
from django.http import JsonResponse
from link.QUESTIONS import QUESTIONS
from .models import LinkModel, LinkType
from user.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
from linkPreview.models import LinkPreviewModel, ParentLink
from survey.models import QuestionPage, QuestionNew, QuestionType, ChoiceNew
import requests, json
from report.views import updateReportLinkSeenIncrement
from configuration.views import convertLongLinkToShortLink

from django.db import transaction, IntegrityError

# Create your views here.

PREVIEW_BASE_URL = "http://api.linkpreview.net/?key=5cd32a757565b4e17f2a258effb8ae350f8a8062d9a4c&q="


def getNewFakeLinkTarget(user_id, link_target_original):
    return convertLongLinkToShortLink(user_id, link_target_original)

@csrf_exempt
def saveOriginalLink(request):
    if request.method == 'POST':
        user_id = request.META.get('HTTP_USERID', 'XXX')
        # return False if no header found
        if user_id == 'XXX':
            return JsonResponse({'success': False, 'message': 'Did you forget to include a valid user_id in the header?'})
        print('Received request from user_id:', user_id)
        link_text_original = request.POST.get('link_text_original', 'XXX')
        link_text_fake = request.POST.get('link_text_fake', 'XXX')
        link_target_original = request.POST.get('link_target_original', 'XXX')
        link_target_fake= request.POST.get('link_target_fake', 'XXX')
        authored_text_original = request.POST.get('authored_text_original', 'XXX')
        authored_text_fake = request.POST.get('authored_text_fake', 'XXX')
        link_image_src_original = request.POST.get('link_image_src_original', 'XXX')
        link_type = request.POST.get('link_type', 'XXX')
        author_name = request.POST.get('author_name', 'XXX')
        is_clicked = request.POST.get('is_clicked', 'False')
        is_seen = bool(request.POST.get('is_seen', 'XXX'))
        # this field is used to maintain the state of the front end hyperfeed (simply specific facebook post) that is being currently stored
        # we simply return this id back to the requesting service without doing anything with it
        hyperfeed_post_id = request.POST.get('hyperfeed_post_id', 'XXX')

        print('received: ',
              'link_text_original:', str(link_text_original), ", ",
              'link_text_fake:', str(link_text_fake), ", ",
              "link_target_original:", str(link_target_original), ", ",
              "link_target_fake:", str(link_target_fake), ", ", end=", ")
        print('authored_text_original:', str(authored_text_original),
              ", link_image_src_original:", str(link_image_src_original),
              ", link_type:", str(link_type), end=", ")
        print('authored_text_fake:', str(authored_text_fake), end=", ")
        print('author_name:', str(author_name), end=", ")
        print('is_clicked:', is_clicked, ", is_seen:", is_seen)
        import re
        if re.match("^[fF]", is_clicked):
            print("is_clicked is false" )
            is_clicked = False
        else:
            print("is_clicked is true")
            is_clicked = True

        facebookLinkTrackingPrependedUrl = "https://l.facebook.com/l.php?u="
        # getrid of the prepended https://l.facebook.com/l.php?u= from the origin link
        link_target_original = str(link_target_original).replace(facebookLinkTrackingPrependedUrl, "")
        # a LinkPreviewModel is the model data for the post related to only fake posts
        # this model data (title, image, link) will be shown to the user during the study
        # to help them recollect what fake post they saw
        # Each LinkPreviewModel is binded to one unique ParentLink which is the actual fake
        # link that uniquely identifies that LinkPreviewModel

        # check if the preview data for this particular link_target_fake is available in the database
        # we try to keep it cached in the db to avoid frequent creation
        parentLink = ParentLink.objects.filter(parent_link=link_target_fake)
        newLinkPreviewModel = None
        if not parentLink:
            print("saveOriginalLink(): parentLink: not found for", link_target_fake)
            # this means that there no valid mapping for this parent link
            # hence an API call needs to be made to get and store its preview data
            # create new parent link
            newParentLink = ParentLink(parent_link = link_target_fake)
            # add this parent link to database
            newParentLink.save()
            print("saveOriginalLink(): newParentLink saved: success: ", newParentLink)

            # get the API data for this parent link
            requestUrl = PREVIEW_BASE_URL + link_target_fake
            print("saveOriginalLink(): requestUrl: ", requestUrl)
            r = requests.get(requestUrl)
            responseMap = json.loads(r.text)
            # create a new link preview model
            newLinkPreviewModel = LinkPreviewModel(parent_link = newParentLink, title = responseMap['title'], description = responseMap['description'], image = responseMap['image'], url = responseMap['url'])
            newLinkPreviewModel.save()
            print("saveOriginalLink(): newLinkPreviewModel saved: success: ", newLinkPreviewModel)
        else:
            print("saveOriginalLink(): parentLink: found for", link_target_fake)
            # get the link preview model associated with this parent link
            newLinkPreviewModel = LinkPreviewModel.objects.filter(parent_link = parentLink[0])
            if not newLinkPreviewModel:
                print("saveOriginalLink(): newLinkPreviewModel: not found for", parentLink)
                return JsonResponse({'success': False, 'message': 'could not restore saved newLinkPreviewModel'})
            newLinkPreviewModel = newLinkPreviewModel[0]

        print('preview_title:', newLinkPreviewModel.title, ", preview_description:", newLinkPreviewModel.description)
        print('preview_image:', newLinkPreviewModel.image, ", preview_url:", newLinkPreviewModel.url)

        matchingUsers = User.objects.filter(uuid=user_id)
        if not matchingUsers:
            # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
            matchingUsers = User.objects.filter(pk=user_id)
        mUser = matchingUsers[0]

        genuineLinkTypeId = 1
        link_type = int(link_type)
        
        # create a new fake link target for genuine link types to later track clicks back to this link model
        if link_type == genuineLinkTypeId:
            old_link_target_fake = link_target_original
            link_target_fake = getNewFakeLinkTarget(user_id, link_target_original)
            print("genuineLinkTypeId found!, added changed link_target_fake from: {", old_link_target_fake, "}", " to {", link_target_fake, "}")

        linkTypeObject = LinkType.objects.filter(pk=int(link_type))[0]
        origLinkModel = LinkModel(link_text_original = link_text_original, link_text_fake = link_text_fake,
                                  link_target_original = link_target_original, link_target_fake = link_target_fake, link_image_src_original = link_image_src_original,
                                  link_type = linkTypeObject, authored_text_original = authored_text_original,
                                  authored_text_fake = authored_text_fake, author_name = author_name,
                                  is_seen = is_seen, is_clicked = is_clicked, time_to_view = datetime.datetime.now().time(),
                                  shown_date_and_time = datetime.datetime.now(),
                                  user = mUser,
                                  preview_title  = newLinkPreviewModel.title,
                                  preview_description = newLinkPreviewModel.description,
                                  preview_image = newLinkPreviewModel.image,
                                  preview_url = newLinkPreviewModel.url)
        # save the model
        origLinkModel.save()
        print("XXX: creating new page")
        # also save a new question page
        # create a new question page and add to question page list
        newQuestionPage = QuestionPage(user=mUser, link_model=origLinkModel)
        # save this question page
        newQuestionPage.save()
        updateReportLinkSeenIncrement(mUser)
        print("XXX: created and saved new page: " + str(newQuestionPage))
        print("XXX: added new empty questionPage successfully!")
        # We now create a second link model that is then used to create a second question page for link models
        # that were faked. That is the value of link_type == 3. The primary idea is that we now want to show
        # both the original link as well as the fake link in the survye pages for all questions that are faked
        # previously we only showed one question page per un-faked(link_type==1) and fake link (link_type==3).
        # Now we plan to add one more question page for the faked links.
        if (int(link_type) == 3):
            # add a link model with the same contents as the fake link model but with link_type==1(genuine) and a newly generate value for link_target_fake
            # this new fake link target will later be used to track clicks back to this link model for all genuine links
            link_target_fake = getNewFakeLinkTarget(user_id, link_target_original)
            linkTypeObject = LinkType.objects.filter(pk=genuineLinkTypeId)[0]
            link_type = genuineLinkTypeId
            linkModelForOriginalLinkOfFakedPosts = LinkModel(link_text_original = link_text_original, link_text_fake = link_text_fake,
                                  link_target_original = link_target_original, link_target_fake = link_target_fake, link_image_src_original = link_image_src_original,
                                  link_type = linkTypeObject, authored_text_original = authored_text_original,
                                  authored_text_fake = authored_text_fake, author_name = author_name,
                                  is_seen = is_seen, is_clicked = is_clicked, time_to_view = datetime.datetime.now().time(),
                                  shown_date_and_time = datetime.datetime.now(),
                                  user = mUser,
                                  preview_title  = newLinkPreviewModel.title,
                                  preview_description = newLinkPreviewModel.description,
                                  preview_image = newLinkPreviewModel.image,
                                  preview_url = newLinkPreviewModel.url)
            print("XXX2: creating an additional question page")
            linkModelForOriginalLinkOfFakedPosts.save()
            print("XXX2: saved new genuine link model", linkModelForOriginalLinkOfFakedPosts)
            # save a new question page
            newQuestionPage = QuestionPage(user=mUser, link_model=linkModelForOriginalLinkOfFakedPosts)
            newQuestionPage.save()
            updateReportLinkSeenIncrement(mUser)
            print("XXX2: created and saved new page: " + str(newQuestionPage))

        return JsonResponse({'success': True, 'message': 'Link saved successfully', 'link_type': link_type, 'link_target_fake': link_target_fake, 'hyperfeed_post_id': hyperfeed_post_id})

    # otherwise return False
    return JsonResponse({'success': False, 'message': 'Invalid request'})