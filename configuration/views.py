from django.shortcuts import render
from .models import Configuration
import json
from django.http import JsonResponse

def getConfiguration(request):
    """
    Return the configuration including chances of cloning
    """
    if request.method == 'GET':
        chancesOfCloning = Configuration.objects.values('chances_of_cloning')
        shouldShowRedBanner =  Configuration.objects.values('should_show_red_banner_for_injected_posts')
        print("chances of cloning: ", str(type(chancesOfCloning)), str(chancesOfCloning[len(chancesOfCloning)-1]))
        print("shouldShowRedBanner ", str(type(shouldShowRedBanner )), str(shouldShowRedBanner[len(shouldShowRedBanner)-1]))

        # get the last key and last value from the saved model
        key1, value1 = next(iter(chancesOfCloning[len(chancesOfCloning)-1])), next(iter(chancesOfCloning[len(chancesOfCloning)-1].values()))

        key2, value2 = next(iter(shouldShowRedBanner[len(shouldShowRedBanner)-1])), next(iter(shouldShowRedBanner[len(shouldShowRedBanner)-1].values()))
        response = {
               key1:value1,
               key2:value2
               } 
        return JsonResponse(response, safe=False)






