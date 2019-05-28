from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from linkPreview.models import ParentLink, LinkPreviewModel

# Register your models here.
# @admin.register(ParentLink)
# class ParentLinkAdmin(admin.ModelAdmin):
#     list_display = ['parent_link']

class ParentLinkResource(resources.ModelResource):
    """
    Add import export feature to ChoiceNew model
    """
    class Meta:
        model = ParentLink
        fields = ('id', 'parent_link')
        export_order = ('id', 'parent_link')

class ParentLinkAdmin(ImportExportModelAdmin):
    resource_class = ParentLinkResource


# @admin.register(LinkPreviewModel)
# class LinkPreviewModelAdmin(admin.ModelAdmin):
#     list_display = ['title', 'description', 'image', 'url', 'get_parent_link']
#
#     def get_parent_link(self, obj):
#         """
#         Return the parent_link associated with this particular LinkPreviewModel
#         :param obj:
#         :return:
#         """
#         return obj.parent_link.parent_link
#
#     get_parent_link.admin_order_field = 'parent_link'
#     get_parent_link.short_description = 'Parent Link'

class LinkPreviewResource(resources.ModelResource):
    """
    Add import export feature to LinkPreviewModel model
    """
    class Meta:
        model = LinkPreviewModel
        fields = ('id', 'parent_link__id', 'title', 'description', 'image', 'url')
        export_order = ('id', 'parent_link__id', 'title', 'description', 'image', 'url')

class LinkPreviewAdmin(ImportExportModelAdmin):
    resource_class = LinkPreviewResource

admin.site.register(ParentLink, ParentLinkAdmin)
admin.site.register(LinkPreviewModel, LinkPreviewAdmin)
