from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from report.models import BriefSummary, DetailedSummary

class BriefSummaryResource(resources.ModelResource):
    class Meta:
        model = BriefSummary
        field = ('user', 'numberOfLinksSeen', 'numberOfLinksClicked', 'numberOfFakeLinksSeen', 'numberOfFakeLinksClicked', 'numberOfGenuineLinksSeen', 'numberOfGenuineLinksClicked')
        export_order = ('user', 'numberOfLinksSeen', 'numberOfLinksClicked','numberOfFakeLinksSeen', 'numberOfFakeLinksClicked', 'numberOfGenuineLinksSeen', 'numberOfGenuineLinksClicked')

# Register your models here.
class BriefSummaryModelAdmin(ImportExportModelAdmin):
    resource_class =  BriefSummaryResource
    list_display = ['getUserName',  'getNumberOfLinksSeen', 'getNumberOfLinksClicked', 'getNumberOfFakeLinksSeen', 'getNumberOfFakeLinksClicked', 'getNumberOfGenuineLinksSeen', 'getNumberOfGenuineLinksClicked']

    def getNumberOfLinksSeen(self, obj):
        return obj.numberOfLinksSeen

    def getNumberOfLinksClicked(self, obj):
        return obj.numberOfLinksClicked

    def getNumberOfFakeLinksSeen(self, obj):
        return obj.numberOfFakeLinksSeen

    def getNumberOfFakeLinksClicked(self, obj):
        return obj.numberOfFakeLinksClicked

    def getNumberOfGenuineLinksSeen(self, obj):
        return obj.numberOfGenuineLinksSeen

    def getNumberOfGenuineLinksClicked(self, obj):
        return obj.numberOfGenuineLinksClicked

    def getUserName(self, obj):
        return obj.user.name

    getUserName.short_description = 'User name'
    getUserName.admin_order_field = 'user__name'

    getNumberOfLinksSeen.short_description = "Total # of links seen so far"
    getNumberOfLinksSeen.admin_order_field = "numberOfLinksSeen"

    getNumberOfLinksClicked.short_description = "Total # of links clicked"
    getNumberOfLinksClicked.admin_order_field = "numberOfLinksClicked"

    getNumberOfFakeLinksSeen.short_description = "Total # of cloned links seen"
    getNumberOfFakeLinksSeen.admin_order_field = "numberOfFakeLinksSeen"

    getNumberOfFakeLinksClicked.short_description = "Total # of cloned links clicked"
    getNumberOfFakeLinksClicked.admin_order_field = "numberOfFakeLinksClicked"

    getNumberOfGenuineLinksSeen.short_description = "Total # of genuine links seen"
    getNumberOfGenuineLinksSeen.admin_order_field = "numberOfGenuineLinksSeen"

    getNumberOfGenuineLinksClicked.short_description = "Total # of genuine links clicked"
    getNumberOfGenuineLinksClicked.admin_order_field = "numberOfGenuineLinksClicked"

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
