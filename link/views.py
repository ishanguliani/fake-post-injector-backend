from django.shortcuts import render
from django.http import JsonResponse
from .models import LinkModel, LinkType
from user.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

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

        origLinkModel = LinkModel(link_text_original = link_text_original, link_text_fake = link_text_fake,
                                  link_target_original = link_target_original, link_target_fake = link_target_fake,
                                  link_type = LinkType.objects.filter(pk=int(link_type))[0], authored_text_original = authored_text_original,
                                  authored_text_fake = authored_text_fake, author_name = author_name,
                                  is_seen = is_seen, is_clicked = is_clicked, time_to_view = datetime.datetime.now().time(),
                                  user = User.objects.filter(pk=user_id)[0])
        # save the model
        origLinkModel.save()
        return JsonResponse({'success': True, 'message': 'Link saved successfully'})

    # otherwise return False
    return JsonResponse({'success': False, 'message': 'Invalid request'})