from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from report.models import BriefSummary

class BriefSummaryResource(resources.ModelResource):
    class Meta:
        model = BriefSummary
        field = ('user', 'numberOfLinksSeen', 'numberOfLinksClicked')
        export_order = ('user', 'numberOfLinksSeen', 'numberOfLinksClicked')

# Register your models here.
class BriefSummaryModelAdmin(ImportExportModelAdmin):
    resource_class =  BriefSummaryResource
    list_display = ['user', 'numberOfLinksSeen', 'numberOfLinksClicked']

admin.site.register(BriefSummary, BriefSummaryModelAdmin)