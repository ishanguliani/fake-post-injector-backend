from django.shortcuts import render
from django.http import JsonResponse
from .models import LinkModel, LinkType
from user.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
from linkPreview.models import LinkPreviewModel, ParentLink
import requests, json
# Create your views here.

PREVIEW_BASE_URL = "http://api.linkpreview.net/?key=5cd32a757565b4e17f2a258effb8ae350f8a8062d9a4c&q="

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

        # now check if the preview data for this particular link_target_fake is available in the database
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

        origLinkModel = LinkModel(link_text_original = link_text_original, link_text_fake = link_text_fake,
                                  link_target_original = link_target_original, link_target_fake = link_target_fake, link_image_src_original = link_image_src_original,
                                  link_type = LinkType.objects.filter(pk=int(link_type))[0], authored_text_original = authored_text_original,
                                  authored_text_fake = authored_text_fake, author_name = author_name,
                                  is_seen = is_seen, is_clicked = is_clicked, time_to_view = datetime.datetime.now().time(),
                                  user = User.objects.filter(pk=user_id)[0],
                                  preview_title  = newLinkPreviewModel.title,
                                  preview_description = newLinkPreviewModel.description,
                                  preview_image = newLinkPreviewModel.image,
                                  preview_url = newLinkPreviewModel.url)
        # save the model
        origLinkModel.save()
        return JsonResponse({'success': True, 'message': 'Link saved successfully'})

    # otherwise return False
    return JsonResponse({'success': False, 'message': 'Invalid request'})