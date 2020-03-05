from django.contrib import admin
from .models import ChoiceNew, QuestionType, QuestionNew, QuestionPage
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class QuestionTypeResource(resources.ModelResource):
    """
    Add import export feature to QuestionType model
    """
    class Meta:
        model = QuestionType
        fields = ('question_type', 'question_tag')

class QuestionTypeAdmin(ImportExportModelAdmin):
    resource_class = QuestionTypeResource
    list_display = ['question_type', 'question_tag']

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
    list_display = ['id', 'user__id', 'link_model__id', 'is_answered']

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
    list_display = ['id', 'question_text', 'question_type__question_type', 'question_page__id']

class ChoiceResource(resources.ModelResource):
    """
    Add import export feature to ChoiceNew model
    """
    class Meta:
        model = ChoiceNew
        fields = ('id', 'choice_text', 'is_selected', 'question__id', 'question__question_text', 'question__question_type__question_type', 'question__question_type__question_tag', 'question__question_page__id', 'question__question_page__user__id', 'question__question_page__link_model__id',  'question__question_page__link_model__link_text_fake', 'question__question_page__link_model__link_target_original', 'question__question_page__link_model__link_target_fake', 'question__question_page__link_model__link_image_src_original', 'question__question_page__link_model__link_type__type', 'question__question_page__link_model__authored_text_original', 'question__question_page__link_model__authored_text_fake', 'question__question_page__link_model__author_name', 'question__question_page__link_model__is_seen', 'question__question_page__link_model__is_clicked', 'question__question_page__link_model__time_to_view', 'question__question_page__link_model__user__id', 'question__question_page__link_model__user__name', 'question__question_page__link_model__user__email', 'question__question_page__link_model__user__attendance_id', 'question__question_page__link_model__preview_title', 'question__question_page__link_model__preview_description', 'question__question_page__link_model__preview_image', 'question__question_page__link_model__preview_url',  'question__question_page__is_answered', 'question__question_page__user__name', 'question__question_page__user__email', 'question__question_page__user__attendance_id')
        export_order = ('id', 'choice_text', 'is_selected', 'question__id', 'question__question_text', 'question__question_type__question_type', 'question__question_type__question_tag', 'question__question_page__id', 'question__question_page__user__id', 'question__question_page__link_model__id',  'question__question_page__link_model__link_text_fake', 'question__question_page__link_model__link_target_original', 'question__question_page__link_model__link_target_fake', 'question__question_page__link_model__link_image_src_original', 'question__question_page__link_model__link_type__type', 'question__question_page__link_model__authored_text_original', 'question__question_page__link_model__authored_text_fake', 'question__question_page__link_model__author_name', 'question__question_page__link_model__is_seen', 'question__question_page__link_model__is_clicked', 'question__question_page__link_model__time_to_view', 'question__question_page__link_model__user__id', 'question__question_page__link_model__user__name', 'question__question_page__link_model__user__email', 'question__question_page__link_model__user__attendance_id', 'question__question_page__link_model__preview_title', 'question__question_page__link_model__preview_description', 'question__question_page__link_model__preview_image', 'question__question_page__link_model__preview_url',  'question__question_page__is_answered', 'question__question_page__user__name', 'question__question_page__user__email', 'question__question_page__user__attendance_id')

class ChoiceAdmin(ImportExportModelAdmin):
    resource_class = ChoiceResource
    list_display = ['id', 'choice_text', 'is_selected']


admin.site.register(QuestionType, QuestionTypeAdmin)
# admin.site.register(QuestionNew)
admin.site.register(QuestionNew, QuestionAdmin)
# admin.site.register(QuestionPage)
admin.site.register(QuestionPage, QuestionPageAdmin)
# admin.site.register(ChoiceNew)
admin.site.register(ChoiceNew, ChoiceAdmin)
