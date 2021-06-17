from django.shortcuts import render
from django.http import HttpResponse
from user.forms import UserModelForm
from user.models import User
import datetime
from django.http import JsonResponse
# Create your views here.

def showWelcomePage(request):
    d = datetime.datetime.today()
    return render(request, "welcome/welcome.html", {'form' : UserModelForm(), 'date': str(d.month) + "-" + str(d.day) + "-" + str(d.year)})

def signupSuccess(request, id):
    return render(request, "welcome/signup_success.html", {'id' : id})

def signupFailed(request):
    return render(request, "welcome/signup_failed.html")

def checkUserUid(request, uuid):
    print('checkUserUuid(): with uuid', str(uuid))
    response = False
    message = ''
    matchingUsers = User.objects.filter(uuid=uuid)
    if not matchingUsers:
        print('checkUserUuid(): matchinguser not found against uuid, checking with uuid')
        # backwards compatibility check: new system only compares users based on uuid while older system used pk(id)
        matchingUsers = User.objects.filter(pk=uuid)
        if not matchingUsers:
            message = 'No matching user found with the given uuid'
        else:
            pass
    else:
        print('checkUserUid(): matchingUser found: ' + str(matchingUsers[0]))
        message = "found user with uuid" + str(matchingUsers[0].uuid)
        response = True
    print('checkUserUuid(): returning response', str(response), ', message:', message, ',uuid:', str(uuid))
    return JsonResponse({'success': response, "message": message, "uuid": uuid})



