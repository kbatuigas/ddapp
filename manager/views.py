# from django.http import Http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin   # We use this with class-based views
# from django.contrib.auth.forms import UserCreationForm
from manager.models import Person, Campaign, Pc, PersonCampaign
from .forms import RegisterForm


# Take advantage of generic views (e.g. ListView) since they abstract
# common web dev patterns and allow us to write much less code.
# ListView is one of the generic views designed for displaying data
# which is one of the things we want on our home page
class IndexView(LoginRequiredMixin, generic.ListView):
    # Picked Campaign since it looks like this makes it easier to step out to
    # the others (e.g. person campaign, character), based on our data model
    model = Campaign
    # Default for ListView would have been 'manager/campaign_list.html' but we
    # need it to use our index.html instead
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # I guess I don't need to pass IndexView, self in super()? https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-display/#adding-extra-context
        context = super().get_context_data(**kwargs)
        # Show campaigns which logged in user is currently in (either as DM or regular player)
        context['my_campaigns'] = Campaign.objects.filter(personcampaign__user_id_person=self.request.user.id)
        # Show available campaigns that logged in user can sign up for
        context['available_campaigns'] = Campaign.objects.exclude(personcampaign__user_id_person=self.request.user.id)

        return context


class PcDetailView(generic.DetailView):
    model = Pc
    # Django looks for manager/pc_detail.html by default so we need to specify the template name
    template_name = 'manager/character-detail.html'


class PcListView(generic.ListView):
    model = Pc
    template_name = 'manager/characters.html'
    context_object_name = 'my_characters'

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


# class CampaignListView(generic.ListView):
#     model = Campaign
#     template_name = 'manager/characters.html'
#     context_object_name = 'my_characters'
#
#     # https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#dynamic-filtering
#     def get_queryset(self):
#         return Pc.objects.filter(user_id_person=self.request.user.id)


# class CampaignSignUp(CreateView):
#     model = PersonCampaign
#     template_name = 'manager/campaign-signup.html'
#     fields = ["is_dm", "campaign_id_campaign", "notes", "user_id_person",
#               "person_campaign_id"]


# It appears that using generic editing views will still work for this use case
# (e.g. update multiple models) as long as you override the default form_valid method
class CampaignCreate(LoginRequiredMixin, CreateView):
    model = Campaign
    template_name = 'manager/campaign-create.html'
    fields = ["name", "dates", "url", "notes"]
    success_url = '/'

    def form_valid(self, form):
        # 1. Get campaign ID
            # Figure out how to get handle to campaign that was just created
        # 2. Create new PersonCampaign
        # 3. Set campaign ID and user ID and is_dm = True for the new PersonCampaign
        # 4. Save new PersonCampaign
        campaign = form.save()
        # campaign.save()
        person_campaign = PersonCampaign()
        person_campaign.campaign_id_campaign = campaign
        # If you create the campaign, you are the DM and you "own" the campaign
        person_campaign.user_id_person = self.request.user.person
        person_campaign.is_dm = True
        person_campaign.save()

        return super().form_valid(form)


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




