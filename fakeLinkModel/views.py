from django.shortcuts import render
from .models import FakeLinkModel
from configuration.views import convertLongLinkToShortLink

import json
from django.http import JsonResponse
# Create your views here.
def getData(request):
    """
    Return the list of fake link models as json data
    :param request:
    :return:
    """

    if request.method == 'GET':
        it = FakeLinkModel.objects.all().iterator()
        for fakelinkmodel in it:
            # if fakelinkmodel.short_link == '' or "https://seng-research.com/track/https://seng-research.com/track" in fakelinkmodel.short_link:
            fakelinkmodel.short_link = convertLongLinkToShortLink(fakelinkmodel.fake_link)
            fakelinkmodel.save()

        return JsonResponse(list(FakeLinkModel.objects.values()), safe=False)

