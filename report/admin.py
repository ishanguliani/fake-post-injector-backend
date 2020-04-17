from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from report.models import BriefSummary, DetailedSummary

class BriefSummaryResource(resources.ModelResource):
    class Meta:
        model = BriefSummary
        field = ('user', 'numberOfLinksSeen', 'numberOfLinksClicked')
        export_order = ('user', 'numberOfLinksSeen', 'numberOfLinksClicked')

# Register your models here.
class BriefSummaryModelAdmin(ImportExportModelAdmin):
    resource_class =  BriefSummaryResource
    list_display = ['user', 'numberOfLinksSeen', 'numberOfLinksClicked']

class DetailedSummaryResource(resources.ModelResource):
    class Meta:
        model = DetailedSummary
        field = ('user', 'linkmodel')
        export_order = ('user', 'linkmodel')

# Register your models here.
class DetailedSummaryModelAdmin(ImportExportModelAdmin):
    resource_class =  DetailedSummaryResource
    list_display = ('user', 'linkmodel')

admin.site.register(BriefSummary, BriefSummaryModelAdmin)
admin.site.register(DetailedSummary, DetailedSummaryModelAdmin)