from django.shortcuts import render
from .models import FakeLinkModel
from configuration.views import convertLongLinkToShortLink

import json
from django.http import JsonResponse
# Create your views here.
def getFakeLinksData(request):
    """
    Return the list of fake link models as json data
    :param request:
    :return:
    """

    if request.method == 'GET':
        user_id = request.META.get('HTTP_USERID', 'XXX')
        # return False if no header found
        if user_id == 'XXX':
            return JsonResponse({'success': False, 'message': 'Did you forget to include a valid user_id in the header?'})
        print('Received request from user_id:', user_id)

        it = FakeLinkModel.objects.all().iterator()
        for fakelinkmodel in it:
                if fakelinkmodel.short_link == '':
                    # fakelinkmodel.short_link = createStringHash(fakelinkmodel.fake_link)
                    fakelinkmodel.short_link = convertLongLinkToShortLink(user_id, fakelinkmodel.fake_link)
                    fakelinkmodel.save()

        return JsonResponse(list(FakeLinkModel.objects.values()), safe=False)

