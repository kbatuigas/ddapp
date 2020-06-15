from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from manager.models import Person, Campaign
from .forms import RegisterForm

# Take advantage of generic views (e.g. ListView) since they abstract
# common web dev patterns and allow us to write much less code.
# ListView is one of the generic views designed for displaying data
# which is one of the things we want on our home page
class IndexView(generic.ListView):
    # Picked Campaign since it looks like this makes it easier to step out to
    # the others (e.g. person campaign, character), based on our data model
    model = Campaign
    context_object_name = 'campaign_list'   # I think this might be ok to get rid of

    # Default for ListView would have been 'manager/campaign_list.html' but we
    # need it to use our index.html instead
    template_name = 'index.html'

    # def get_queryset(self):
    #     return Campaign.objects.all()

# Form data is validated and db is refreshed after the signal so that the corresponding
# person instance created by the signal is loaded. Then the custom person fields are saved
# to the user model, after which the person/user is logged in and redirected to the home page
# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            # There is a synchronism issue here where the corresponding Person is created but
            # the User model here doesn't have access to the Person fields we want to save to.
            # So we use refresh_from_db() to reload the database and load the Person instance
            user.refresh_from_db()
            user.person.birthdate = form.cleaned_data.get('birthdate')
            user.person.discord_id = form.cleaned_data.get('discord_id')
            user.person.zoom_id = form.cleaned_data.get('zoom_id')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(response, user)

            return redirect('/')
    else:
        form = RegisterForm()

    return render(response, 'manager/register.html', {'form': form})




