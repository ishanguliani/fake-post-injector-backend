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
            data = newUser.save()
            print("XXX: passing id: ", data.id)
            return HttpResponseRedirect(reverse('signupSuccess', args=(data.id, )))
            # return redirect('/signup-success/', theId=data.id)
        else:
            return redirect('/signupFailed/')
    return JsonResponse({"success": False, "message" : "something went wrong in saving the user"})

def getUser(request):
    pass