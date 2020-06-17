from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from manager.models import Pc


class RegisterForm(UserCreationForm):
	# Specify the extra Person fields we want to be able to save to upon registration
	birthdate = forms.DateField()
	discord_id = forms.CharField(max_length=100, help_text='Discord ID')
	zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')

	class Meta:
		model = User
		fields = ["username", "password1", "password2", "birthdate", "email", "discord_id",
				  "zoom_id"]


# Create a Form class from a Pc model
# class CreateNewCharacterForm(ModelForm):
# 	class Meta:
# 		model = Pc
# 		# It's better practice to explicitly set all fields that should be edited
# 		fields = ["name", "class_level", "id_pc_class", "id_alignment", "id_race", "strength",
# 				  "dexterity", "constitution", "intelligence", "wisdom", "charisma", "armor_class",
# 				  "initiative", "hp", "xp", "equipment", "spells", "treasure"]


	# name = forms.CharField()
	# level = forms.IntegerField()
	# pc_class = forms.
	# alignment =
	# race =
