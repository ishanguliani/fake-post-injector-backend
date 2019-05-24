from django import forms
from .models import Question

class SurveyModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        # labels = {
        #     'question_text': '',
        #     'email': 'Your email',
        #     'attendance_id': 'Attendance id provided by the survey incharge',
        # }
        # help_texts = {
        #     'name': 'Your name',
        #     'email': 'Your email',
        #     'attendance_id': 'Attendance id provided by the survey incharge',
        # }