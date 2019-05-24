from django.shortcuts import render
from .models import FakeLinkModel
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
        allFakeLinks = FakeLinkModel.objects.all()
        allFakeLinksValues = list(FakeLinkModel.objects.values())
        # print('allFakeLinksValues', allFakeLinksValues )
        print("type(allFakeLinks)", type(allFakeLinks))
        print("allFakeLinks", allFakeLinks)
        return JsonResponse(allFakeLinksValues, safe=False)

