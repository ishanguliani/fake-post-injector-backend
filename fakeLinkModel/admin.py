from django.contrib import admin
from .models import FakeLinkModel
# Register your models here.
@admin.register(FakeLinkModel)
class FakeLinkModelAdmin(admin.ModelAdmin):
    list_display = ['fake_picture', 'fake_link_text', 'fake_link_description', 'fake_link', 'fake_link_header']