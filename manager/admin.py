from django.contrib import admin

from .models import Person, Campaign, PersonCampaign, Pc, PcClass, Alignment, Race

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'dates', 'rating', 'url')
    fields = ['name', 'dates', 'rating', 'url', 'notes']


admin.site.register(Person)
# admin.site.register(Campaign)
admin.site.register(PersonCampaign)
admin.site.register(Pc)
admin.site.register(PcClass)
admin.site.register(Alignment)
admin.site.register(Race)