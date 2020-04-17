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
        allFakeLinksValues = list(FakeLinkModel.objects.values())
        for fakelinkmodel in allFakeLinksValues:
            if fakelinkmodel.short_link == '':
                fakelinkmodel.short_link = "https://seng-research.com/track/" + convertLongLinkToShortLink(fakelinkmodel.fake_link)
                fakelinkmodel.save()
        # print('allFakeLinksValues', allFakeLinksValues )
        return JsonResponse(allFakeLinksValues, safe=False)

