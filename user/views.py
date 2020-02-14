from django.shortcuts import render, redirect, reverse
from .forms import UserModelForm
from .models import User
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
def createUser(request):
    if request.method == 'POST':
        newUser = UserModelForm(request.POST or None)
        if newUser.is_valid():
            # form is valid, save it
            newUser.setUuid()
            newUser = newUser.save()
            uuid = newUser.uuid
            print("XXX: passing uuid: ", uuid)
            return HttpResponseRedirect(reverse('signupSuccess', args=(uuid, )))
            # return redirect('/signup-success/', theId=data.id)
        else:
            return redirect('/signupFailed/')
    return JsonResponse({"success": False, "message" : "something went wrong in saving the user"})

def getUser(request):
    pass