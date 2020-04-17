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
        print('got iterator')
        for fakelinkmodel in it:
            if fakelinkmodel.short_link == '' or fakelinkmodel.short_link.contains("https://seng-research.com/track/https://seng-research.com/track"):
                fakelinkmodel.short_link = convertLongLinkToShortLink(fakelinkmodel.fake_link)
                fakelinkmodel.save()

        allFakeLinksValues = list(FakeLinkModel.objects.values())
        # print('type of FakeLinkModel.objects.values()', type(FakeLinkModel.objects.values()))
        # print('type of FakeLinkModel.objects.values()[0]', type(FakeLinkModel.objects.values()[0]))
        # print('FakeLinkModel.objects.values()[0]', FakeLinkModel.objects.values()[0])
        # for fakelinkmodel in allFakeLinksValues:
        #     if fakelinkmodel["short_link"] == '':
        #         fakelinkmodel.short_link = "https://seng-research.com/track/" + convertLongLinkToShortLink(fakelinkmodel.fake_link)
        #         fakelinkmodel.save()
        # print('allFakeLinksValues', allFakeLinksValues )
        return JsonResponse(allFakeLinksValues, safe=False)

