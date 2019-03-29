from django.contrib import admin
from link.models import LinkModel, LinkType

# Register your models here.
@admin.register(LinkModel)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['link_text', 'post_text', 'user', 'seen_status', 'clicked_status']

@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ['type']