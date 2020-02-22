from django import forms
from .models import User

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'attendance_id']

        labels = {
            'name': 'What do we call you? (Name)',
            'email': 'How do we reach you? (Email id)',
            'attendance_id': 'Enter the attendance id provided to you today',
        }
        help_texts = {
            'name': 'Type your name',
            'email': 'Type your email',
            # 'attendance_id': 'Attendance id provided by the survey incharge',
        }



