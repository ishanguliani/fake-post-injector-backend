from django.shortcuts import render

# Create your views here.
def trackLink(request, short_link):
    """
    count this link click and route the user to the appropriate link
    """
    if request.method == 'GET':
        pass
