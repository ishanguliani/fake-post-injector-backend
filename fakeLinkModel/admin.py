from django.contrib import admin
from .models import FakeLinkModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# @admin.register(FakeLinkModel)
# class FakeLinkModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'fake_picture', 'fake_link_topic', 'fake_link_text', 'fake_link_description', 'fake_link', 'fake_link_header']

class FakeLinkModelResource(resources.ModelResource):
    """
    Add import export feature to FakeLinkModel model
    """
    class Meta:
        model = FakeLinkModel
        fields = ('id', 'fake_picture', 'fake_link_topic', 'fake_link_text', 'fake_link_description', 'fake_link', 'fake_link_header',  'string_hash')
        export_order = ('id', 'fake_picture', 'fake_link_topic', 'fake_link_text', 'fake_link_description', 'fake_link', 'fake_link_header',  'string_hash')

class FakeLinkModelAdmin(ImportExportModelAdmin):
    resource_class = FakeLinkModelResource
    list_display = ['id', 'fake_picture', 'fake_link_topic', 'fake_link_text', 'fake_link_description', 'fake_link', 'fake_link_header', 'string_hash']
    readonly_fields = ['id', 'string_hash']

admin.site.register(FakeLinkModel, FakeLinkModelAdmin)