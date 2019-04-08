from django.contrib import admin
from link.models import LinkModel, LinkType

# Register your models here.
@admin.register(LinkModel)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['link_text_original', 'link_text_fake', 'link_target_original', 'link_target_fake', 'link_type', 'authored_text_original', 'authored_text_fake', 'author_name', 'is_seen', 'is_clicked', 'user']

@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ['type']