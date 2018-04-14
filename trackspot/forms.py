from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class user_profile_form(forms.Form):
	display_name = forms.CharField(help_text="Your name.", max_length=50)
	location = forms.CharField(help_text="Your city or town.", max_length=50)
	bio = forms.CharField(help_text="Optional Bio", max_length=500)

