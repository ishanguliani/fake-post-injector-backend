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
        print("chances of cloning: ", str(type(chancesOfCloning)), str(chancesOfCloning))
        return JsonResponse(chancesOfCloning[len(chancesOfCloning)-1], safe=False)




        
        
