from django.contrib import admin
from user.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'attendance_id']

class UserResource(resources.ModelResource):
    """
    Add import export feature to ChoiceNew model
    """
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'attendance_id')
        export_order = ('id', 'name', 'email', 'attendance_id')

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

admin.site.register(User, UserAdmin)