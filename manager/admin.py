from django.contrib import admin

from .models import Person, Campaign, PersonCampaign, Pc, PcClass, Alignment, Race

# Register your models here.

# @admin.register(Campaign)
# class

admin.site.register(Person)
admin.site.register(Campaign)
admin.site.register(PersonCampaign)
admin.site.register(Pc)
admin.site.register(PcClass)
admin.site.register(Alignment)
admin.site.register(Race)