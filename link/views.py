from django.shortcuts import render
from django.http import JsonResponse
from .models import LinkModel
from user.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def saveOriginalLink(request):
    if request.method == 'POST':
        # get the link
        if 'link' in request.POST:
            theLink = request.POST['link']
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
        """
        link_text = models.CharField(max_length=100, blank=True)
        link_target = models.CharField(max_length=100, blank=True)
        post_text = models.CharField(max_length=100, blank=True)
        author_name = models.CharField(max_length=100, blank=True)
        seen_status = models.BooleanField(default=False)
        user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        """
        origLinkModel = LinkModel(link_text = theLink, link_target = theLink, post_text = "This is microsoft cloud",
                                  author_name = "Ishan Guliani", clicked_status = False, seen_status = True, user = User.objects.filter(pk=9)[0], time_to_view = datetime.datetime.now().time())
        # save the model
        origLinkModel.save()
        return JsonResponse({'success': True, 'message':'Link saved successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})