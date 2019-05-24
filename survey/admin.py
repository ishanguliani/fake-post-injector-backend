from django.contrib import admin
from .models import Question, Choice, ChoiceNew, QuestionType, QuestionNew, QuestionPage

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['question_type', 'question_tag']

# admin.site.register(Question)
admin.site.register(QuestionNew)
admin.site.register(QuestionPage)
# admin.site.register(Choice)
admin.site.register(ChoiceNew)
