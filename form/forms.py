from django import forms
from .models import Product

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', ]
        labels = {
            'title': 'What do we call you?',
            'descrption': 'Type your name here',
        }
        help_texts = {
            'title': 'How do we reach you?',
            'description': 'Type your email here',
        }