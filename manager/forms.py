from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django.core import validators
from manager.models import Campaign, Pc, PersonCampaign


class CharactersModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		curr_campaign = str(obj.campaign_id_campaign) 	# Why does this work?? Would have expected ID value and not the Campaign obj

		return "{character}{in_campaign}".format(character=obj, in_campaign=" (Currently in " + curr_campaign + ")" if obj.campaign_id_campaign else "")


class CampaignSignUpForm(forms.Form):
	# Only include campaigns that have not been signed up for yet, i.e.
	# where campaign.campaign_id is not in the set of person_campaign.campaign_id_campaign values
	# that belong to user_id_person = request.user. Define queryset in __init__ below
	campaign = forms.ModelChoiceField(queryset=None, label='Select the campaign you want to join')
	# Since a character can only be in one campaign at a time,
	# Only include characters that have not been signed up to a campaign yet, i.e.
	# where pc.user_id_person = request.user and pc.campaign_id_campaign is null?
	# Define queryset in __init__ below
	characters = CharactersModelChoiceField(queryset=None, label='Select the characters you want to play '
																	'for this campaign')

	# The form doesn't have access to the request so we can't just say request.user in the queryset definition above
	# Override the init method to pass in the request.user and reference it in the form field
	def __init__(self, *args, **kwargs):
		self.person = kwargs.pop('person')
		super(CampaignSignUpForm, self).__init__(*args, **kwargs)
		self.fields['campaign'].queryset = Campaign.objects.exclude(pk__in=PersonCampaign.objects.values_list('campaign_id_campaign', flat=True).filter(user_id_person=self.person))
		self.fields['characters'].queryset = Pc.objects.filter(user_id_person=self.person,)


class RegisterForm(UserCreationForm):
	# Specify the extra Person fields we want to be able to save to upon registration
	birthdate = forms.DateField()
	discord_id = forms.CharField(max_length=100, help_text='Discord ID')
	zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')

	class Meta:
		model = User
		fields = ["username", "password1", "password2", "birthdate", "email", "discord_id",
				  "zoom_id"]



