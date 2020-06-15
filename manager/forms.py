from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators


class RegisterForm(UserCreationForm):
	# Specify the extra Person fields we want to be able to save to upon registration
	birthdate = forms.DateField()
	discord_id = forms.CharField(max_length=100, help_text='Discord ID')
	zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')

	class Meta:
		model = User
		fields = ["username", "password1", "password2", "birthdate", "email", "discord_id",
				  "zoom_id"]