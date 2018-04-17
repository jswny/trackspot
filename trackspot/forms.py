from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class review_form(forms.Form):
	description = forms.CharField(help_text= "What did you think?", max_length = 500)
	rating = forms.IntegerField(help_text = "From 0 to 100", max_value = 100)
	#user = forms.CharField(help_text = "Your User ID", max_length = 100)
	#song = forms.CharField(help_text = "Name of Song", max_length = 100)
	#album = forms.CharField(help_text = "Name of Album", max_length = 100)

class edit_profile_form(forms.Form):
	name = forms.CharField(help_text="Your name.", max_length=50)
	location = forms.CharField(help_text="Your city or town.", max_length=50)
	bio = forms.CharField(help_text="Bio (Max 500 characters)", max_length=500)
	profile_pic = forms.URLField(help_text="Enter an image URL", max_length=500)

class edit_critic_form(forms.Form):
	name = forms.CharField(help_text="Your name.", max_length=50)
	location = forms.CharField(help_text="Your city or town.", max_length=50)
	bio = forms.CharField(help_text="Bio (Max 500 characters)", max_length=500)
	profile_pic = forms.URLField(help_text="Enter an image URL", max_length=500)
	organization = forms.CharField(help_text="Enter your organization", max_length=50)
