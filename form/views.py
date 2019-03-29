# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import MessageForm
from .models import Product
from .forms import ProductModelForm
from django.http import JsonResponse


def showForm(request):
    # This view is missing all form handling logic for simplicity of the example
    # return render(request, 'form.html', {'form': MessageForm()})
    # return JsonResponse({'foo': 'bar'})
    return render(request, "form/form.html", {'form': ProductModelForm()})

def product_detail_view(request):
    # if request.GET == "GET":
        # this is a get request
    aProduct = Product.objects.get(id=1)
    context = {
        'object': aProduct
    }

    return render(request, 'form/form.html', context)

def product_model_form(request):
    form = ProductModelForm(request)
    # create a new model form
    if request.method == 'POST':
        if form.is_valid():
            print('form is valid')
            form.save()
    else:
        # create a context
        context = {
            'form': form
        }

        # return render(request, "form/form.html", context)
