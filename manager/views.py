# from django.http import Http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin   # We use this with class-based views
# from django.contrib.auth.forms import UserCreationForm
from manager.models import Person, Campaign, Pc
from .forms import RegisterForm


# Take advantage of generic views (e.g. ListView) since they abstract
# common web dev patterns and allow us to write much less code.
# ListView is one of the generic views designed for displaying data
# which is one of the things we want on our home page
class IndexView(LoginRequiredMixin, generic.ListView):
    # Picked Campaign since it looks like this makes it easier to step out to
    # the others (e.g. person campaign, character), based on our data model
    model = Campaign
    context_object_name = 'campaign_list'   # I think this might be ok to get rid of

    # Default for ListView would have been 'manager/campaign_list.html' but we
    # need it to use our index.html instead
    template_name = 'index.html'


class PcDetailView(generic.DetailView):
    model = Pc
    # Django looks for manager/pc_detail.html by default so we need to specify the template name
    template_name = 'manager/character-detail.html'


class PcListView(generic.ListView):
    model = Pc
    template_name = 'manager/characters.html'
    context_object_name = 'my_characters'
    # TODO: I think I need to define queryset so that it returns only characters where person is the
    #   logged in user

    # https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#dynamic-filtering
    def get_queryset(self):
        return Pc.objects.filter(user_id_person=self.request.user.id)


class PcCreate(LoginRequiredMixin, CreateView):
    model = Pc
    template_name = 'manager/character-new.html'
    # It's better practice to explicitly set all fields that should be edited
    fields = ["name", "class_level", "id_pc_class", "id_alignment", "id_race", "strength",
              "dexterity", "constitution", "intelligence", "wisdom", "charisma", "armor_class",
              "initiative", "hp", "xp", "equipment", "spells", "treasure"]
    success_url = reverse_lazy('characters')

    def form_valid(self, form):
        form.instance.user_id_person = self.request.user.person
        return super().form_valid(form)


class PcUpdate(UpdateView):
    model = Pc
    template_name = 'manager/character-edit.html'
    fields = ["name", "class_level", "id_pc_class", "id_alignment", "id_race", "strength",
              "dexterity", "constitution", "intelligence", "wisdom", "charisma", "armor_class",
              "initiative", "hp", "xp", "equipment", "spells", "treasure"]


# Form data is validated and db is refreshed after the signal so that the corresponding
# person instance created by the signal is loaded. Then the custom person fields are saved
# to the user model, after which the person/user is logged in and redirected to the home page
# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
@login_required
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

            return redirect('/')    # Make sure this is inside the if block
    else:
        form = RegisterForm()

    return render(response, 'manager/register.html', {'form': form})




