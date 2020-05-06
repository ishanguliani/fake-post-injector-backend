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
    list_display = ['getUserName',  'getNumberOfLinksSeen', 'getNumberOfLinksClicked']

    def getNumberOfLinksSeen(self, obj):
        return obj.numberOfLinksSeen

    def getNumberOfLinksClicked(self, obj):
        return obj.numberOfLinksClicked

    def getUserName(self, obj):
        return obj.user.name

    getUserName.short_description = 'User name'
    getUserName.admin_order_field = 'user__name'

    getNumberOfLinksSeen.short_description = "Total # of links seen so far"
    getNumberOfLinksSeen.admin_order_field = "numberOfLinksSeen"

    getNumberOfLinksClicked.short_description = "Total # of links clicked"
    getNumberOfLinksClicked.admin_order_field = "numberOfLinksClicked"

class DetailedSummaryResource(resources.ModelResource):
    class Meta:
        model = DetailedSummary
        field = ('user', 'redirectionLink', 'linkModel')
        export_order = ('user', 'redirectionLink', 'linkModel')

# Register your models here.
class DetailedSummaryModelAdmin(ImportExportModelAdmin):
    resource_class =  DetailedSummaryResource
    list_display = ('getUserName', 'getRedirectionLink', 'getShortLink', 'getLinkType', 'getOriginalLink')

    def getUserName(self, obj):
        return obj.user.name

    def getRedirectionLink(self, obj):
        return obj.redirectionLink

    def getShortLink(self, obj):
        return obj.linkModel.link_target_fake

    def getLinkType(self, obj):
        return obj.linkModel.link_type

    def getOriginalLink(self, obj):
        return obj.originalLinkThatWasFaked

    getUserName.short_description = 'User name'
    getUserName.admin_order_field = 'user__name'

    getRedirectionLink.short_description = 'User redirected to'
    getRedirectionLink.admin_order_field = 'redirectionLink'

    getShortLink.short_description = 'Clicked on'
    getShortLink.admin_order_field = 'linkModel__link_target_fake'

    getLinkType.short_description = "Link type"
    getLinkType.admin_order_field = 'linkModel__link_type'

    getOriginalLink.short_description = "Original link that was faked"
    getOriginalLink.admin_order_field = "originalLinkThatWasFaked"


admin.site.register(BriefSummary, BriefSummaryModelAdmin)
admin.site.register(DetailedSummary, DetailedSummaryModelAdmin)
