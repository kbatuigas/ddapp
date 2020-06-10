from django.shortcuts import render
# from django.views import generic

# Create your views here.
from django.views import generic

from manager.models import Person, Campaign

class IndexView(generic.ListView):
    model = Campaign
    context_object_name = 'campaign_list'
    template_name = 'index.html'

    # def get_queryset(self):
    #     return Campaign.objects.all()






