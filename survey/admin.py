from django.contrib import admin
from .models import ChoiceNew, QuestionType, QuestionNew, QuestionPage
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# @admin.register(QuestionType)
# # class QuestionTypeAdmin(admin.ModelAdmin):
# class QuestionTypeAdmin(resources.ModelResource):
#     list_display = ['question_type', 'question_tag']

class QuestionTypeResource(resources.ModelResource):
    """
    Add import export feature to QuestionType model
    """
    class Meta:
        model = QuestionType
        fields = ('question_type', 'question_tag')

class QuestionTypeAdmin(ImportExportModelAdmin):
    resource_class = QuestionTypeResource

class QuestionPageResource(resources.ModelResource):
    """
    Add import export feature to QuestionPage model
    """
    class Meta:
        model = QuestionPage
        fields = ('id', 'user__id', 'link_model__id', 'is_answered')
        export_order = ('id', 'user__id', 'link_model__id', 'is_answered')

class QuestionPageAdmin(ImportExportModelAdmin):
    resource_class = QuestionPageResource

class QuestionResource(resources.ModelResource):
    """
    Add import export feature to QuestionNew model
    """
    class Meta:
        model = QuestionNew
        fields = ('id', 'question_text', 'question_type__question_type', 'question_page__id')
        export_order = ('id', 'question_page__id', 'question_type__question_type', 'question_text')

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

class ChoiceResource(resources.ModelResource):
    """
    Add import export feature to ChoiceNew model
    """
    class Meta:
        model = ChoiceNew
        fields = ('id', 'choice_text', 'is_selected', 'question__id', 'question__question_text', 'question__question_type__question_type', 'question__question_type__question_tag', 'question__question_page__id', 'question__question_page__user__id', 'question__question_page__link_model__id', 'question__question_page_is_answered', 'question__question_page__user__name', 'question__question_page__user__email', 'question__question_page__user__attendance_id')
        export_order = ('id', 'choice_text', 'is_selected', 'question__id', 'question__question_text', 'question__question_type__question_type', 'question__question_type__question_tag', 'question__question_page__id', 'question__question_page__user__id')

class ChoiceAdmin(ImportExportModelAdmin):
    resource_class = ChoiceResource

admin.site.register(QuestionType, QuestionTypeAdmin)
# admin.site.register(QuestionNew)
admin.site.register(QuestionNew, QuestionAdmin)
# admin.site.register(QuestionPage)
admin.site.register(QuestionPage, QuestionPageAdmin)
# admin.site.register(ChoiceNew)
admin.site.register(ChoiceNew, ChoiceAdmin)
