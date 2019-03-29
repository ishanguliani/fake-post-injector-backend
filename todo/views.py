from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.

from .models import TodoItem

def todoView(request):
    allItems = TodoItem.objects.all()
    return render(request, 'todoTemplate.html', {'allItems' : allItems})

def addTodo(request):
    """
    Add a todo item to the DB
    :param request: a post request containing form fields
    :return: HttpResponseRedirect to todo page
    """
    # create a new object
    newObject  = TodoItem(content = request.POST['content'])
    # save a new object
    newObject.save()
    # redirect to an HttpResponseRedirect object
    return HttpResponseRedirect('/todo/')

def deleteTodo(request, todoId):
    """
    Remove a todo item with the given Id from the DB
    :param request: the incoming post request
    :param todoId: the id of the item to delete
    :return: HttpResponseRedirect to todo page
    """
    # get the corresponding object
    toDelete = TodoItem.objects.get(id = todoId)
    # delete the item
    toDelete.delete()
    # redirect to an HttpResponseRedirect object
    return HttpResponseRedirect('/todo/')
