from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from manager.models import Person, Campaign
from .forms import RegisterForm


# Create your views here.

class IndexView(generic.ListView):
    model = Campaign
    context_object_name = 'campaign_list'
    template_name = 'index.html'

    # def get_queryset(self):
    #     return Campaign.objects.all()

def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return redirect('/manager/register/')
    else:
        form = RegisterForm()

    return render(response, 'manager/register.html', {'form': form})




