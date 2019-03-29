from django.shortcuts import render
from django.http import HttpResponse
from user.forms import UserModelForm

# Create your views here.

def showWelcomePage(request):
    return render(request, "welcome/welcome.html", {'form' : UserModelForm()})

def signupSuccess(request, id):
    return render(request, "welcome/signup_success.html", {'id' : id})

def signupFailed(request):
    return render(request, "welcome/signup_failed.html")



