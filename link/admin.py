from django.contrib import admin
from link.models import LinkModel, LinkType
from import_export import resources
from import_export.admin import ImportExportModelAdmin

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
        fields = ('id', 'link_text_original', 'link_text_fake', 'link_target_original', 'link_target_fake', 'link_image_src_original', 'link_type', 'authored_text_original', 'author_name', 'is_seen', 'is_clicked', 'user', 'preview_title', 'preview_description', 'preview_image', 'preview_url', 'time_to_view')
        export_order = ('link_type', 'link_text_original', 'link_text_fake', 'is_clicked',  'user', 'id', 'link_target_original', 'link_target_fake', 'link_image_src_original', 'authored_text_original', 'author_name', 'is_seen', 'preview_title', 'preview_description', 'preview_image', 'preview_url', 'time_to_view')

class LinkModelAdmin(ImportExportModelAdmin):
    resource_class = LinkModelResource
    list_display = ['link_type',  'link_text_original', 'link_text_fake', 'is_clicked', 'user', 'property_link_target_original', 'property_link_target_fake', 'link_image_src_original', 'property_authored_text_original', 'author_name', 'is_seen']
    readonly_fields = ('id', 'link_text_original', 'link_text_fake', 'link_target_original', 'link_target_fake', 'link_image_src_original', 'link_type', 'authored_text_original', 'author_name', 'is_seen', 'is_clicked', 'preview_title', 'preview_description', 'preview_image', 'preview_url', 'time_to_view', 'user')

# @admin.register(LinkType)
# class LinkTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'type']

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

admin.site.register(LinkModel, LinkModelAdmin)
admin.site.register(LinkType, LinkTypeAdmin)
