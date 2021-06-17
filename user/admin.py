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
        export_order = ('id', 'uuid', 'name', 'alias', 'email', 'mturk_id', 'attendance_id', 'date_of_registration')
        fields = ('id', 'uuid', 'name', 'alias', 'email', 'mturk_id', 'attendance_id', 'date_of_registration')

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    readonly_fields = ('id', 'uuid', 'name', 'alias', 'email', 'mturk_id', 'attendance_id', 'date_of_registration')
    list_display = ['id', 'uuid', 'name', 'alias', 'email', 'mturk_id', 'attendance_id', 'date_of_registration']
admin.site.register(User, UserAdmin)
