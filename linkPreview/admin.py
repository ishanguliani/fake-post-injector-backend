from django.contrib import admin
from linkPreview.models import ParentLink, LinkPreviewModel

# Register your models here.
@admin.register(ParentLink)
class ParentLinkAdmin(admin.ModelAdmin):
    list_display = ['parent_link']

@admin.register(LinkPreviewModel)
class LinkPreviewModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image', 'url', 'get_parent_link']

    def get_parent_link(self, obj):
        """
        Return the parent_link associated with this particular LinkPreviewModel
        :param obj:
        :return:
        """
        return obj.parent_link.parent_link

    get_parent_link.admin_order_field = 'parent_link'
    get_parent_link.short_description = 'Parent Link'
