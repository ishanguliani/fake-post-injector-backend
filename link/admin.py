from datetime import datetime

from django.contrib import admin
from link.models import LinkModel, LinkType
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# Register your models here.
# @admin.register(LinkModel)
# class LinkAdmin(admin.ModelAdmin):
#     list_display = ['link_text_original', 'link_text_fake', 'property_link_target_original', 'property_link_target_fake', 'link_image_src_original', 'link_type', 'property_authored_text_original', 'authored_text_fake', 'author_name', 'is_seen', 'is_clicked', 'user']

class LinkModelResource(resources.ModelResource):
    """
    Add import export feature to LinkModel model
    """
    class Meta:
        model = LinkModel
        fields = ('id', 'link_text_original', 'link_text_fake', 'link_target_original', 'link_target_fake', 'link_image_src_original', 'link_type', 'authored_text_original', 'author_name', 'is_seen', 'is_clicked', 'is_clicked_event_from_ground_data', 'is_clicked_event_from_ground_data_time', 'user', 'preview_title', 'preview_description', 'preview_image', 'preview_url', 'shown_date_and_time')
        export_order = ('link_type', 'link_text_original', 'link_text_fake', 'is_clicked', 'is_clicked_event_from_ground_data', 'is_clicked_event_from_ground_data_time', 'user', 'id', 'link_target_original', 'link_target_fake', 'link_image_src_original', 'authored_text_original', 'author_name', 'is_seen', 'preview_title', 'preview_description', 'preview_image', 'preview_url', 'shown_date_and_time')

class LinkModelAdmin(ImportExportModelAdmin):
    resource_class = LinkModelResource
    list_display = ['link_type',  'link_text_original', 'link_text_fake', 'is_clicked', 'is_clicked_event_from_ground_data', 'is_clicked_event_from_ground_data_time', 'shown_date_and_time',  'user', 'property_link_target_original', 'property_link_target_fake', 'link_image_src_original', 'property_authored_text_original', 'author_name', 'is_seen']
    readonly_fields = ('id', 'link_text_original', 'link_text_fake', 'link_target_original', 'link_target_fake', 'link_image_src_original', 'link_type', 'authored_text_original', 'authored_text_fake', 'author_name', 'is_seen', 'is_clicked', 'is_clicked_event_from_ground_data', 'is_clicked_event_from_ground_data_time', 'preview_title', 'preview_description', 'preview_image', 'preview_url', 'shown_date_and_time', 'user')

# @admin.register(LinkType)
# class LinkTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'type']

class LinkModelListFilterAdmin(LinkModelAdmin):
    list_filter = (
        ('shown_date_and_time', DateRangeFilter),
        ('is_clicked_event_from_ground_data_time', DateTimeRangeFilter)
    )

    # If you would like to add a default range filter
    # method pattern "get_rangefilter_{field_name}_default"
    def get_rangefilter_shown_date_and_time_default(self, request):
        return (datetime.date.today, datetime.date.today)

    def get_rangefilter_is_clicked_event_from_ground_data_time_default(self, request):
        return (datetime.date.today, datetime.date.today)

    # If you would like to change a title range filter
    # method pattern "get_rangefilter_{field_name}_title"
    def get_rangefilter_shown_date_and_time_title(self, request, field_path):
        return 'Last shown date'

    def get_rangefilter_is_clicked_event_from_ground_data_time_title(self, request, field_path):
        return 'Last clicked date'



class LinkTypeModelResource(resources.ModelResource):
    """
    Add import export feature to LinkType model
    """
    class Meta:
        model = LinkType
        fields = ('id', 'type')
        export_order = ('id', 'type')

class LinkTypeAdmin(ImportExportModelAdmin):
    resource_class = LinkTypeModelResource
    readonly_fields = ['id', 'type']

admin.site.register(LinkModel, LinkModelListFilterAdmin)
admin.site.register(LinkType, LinkTypeAdmin)
