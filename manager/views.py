from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
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
            user = form.save()
            user.refresh_from_db()
            user.person.birthdate = form.cleaned_data.get('birthdate')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(response, user)

            return redirect('/')
    else:
        form = RegisterForm()

    return render(response, 'manager/register.html', {'form': form})




