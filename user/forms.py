from django import forms
from .models import User

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['alias', 'mturk_id', 'attendance_id']

        labels = {
            'alias': 'Enter your alias',
            'mturk_id': 'Enter your mturk id',
            'attendance_id': 'Enter the attendance id provided to you today',
        }
        help_texts = {
            'alias': 'Type your alias',
            'mturk_id': 'Type your mturk id',
            # 'attendance_id': 'Attendance id provided by the survey incharge',
        }



