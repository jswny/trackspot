from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class edit_profile_form(forms.Form):
	name = forms.CharField(help_text="Your name.", max_length=50)
	location = forms.CharField(help_text="Your city or town.", max_length=50)
	bio = forms.CharField(help_text="Bio (Max 500 characters)", max_length=500)
	profile_pic = forms.URLField(help_text="Enter an image URL", max_length=500)

class review_form(forms.Form):
	review = forms.CharField(help_text = "Review:", max_length = 1000)