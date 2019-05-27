from django.shortcuts import render
from django.http import HttpResponse
from user.forms import UserModelForm
import datetime
# Create your views here.

def showWelcomePage(request):
    d = datetime.datetime.today()
    return render(request, "welcome/welcome.html", {'form' : UserModelForm(), 'date': str(d.month) + "-" + str(d.day) + "-" + str(d.year)})

def signupSuccess(request, id):
    return render(request, "welcome/signup_success.html", {'id' : id})

def signupFailed(request):
    return render(request, "welcome/signup_failed.html")



