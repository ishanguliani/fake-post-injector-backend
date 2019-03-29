from django import forms
from .models import User

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'attendance_id']

        labels = {
            'name': 'Your name',
            'email': 'Your email',
            'attendance_id': 'Attendance id provided by the survey incharge',
        }
        help_texts = {
            'name': 'Your name',
            'email': 'Your email',
            'attendance_id': 'Attendance id provided by the survey incharge',
        }
