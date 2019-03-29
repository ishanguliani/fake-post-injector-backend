from django import forms
from .models import Product

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', ]
        labels = {
            'title': 'Your name',
            'descrption': 'Your email',
        }
        help_texts = {
            'title': 'Your name',
            'description': 'Your email',
        }