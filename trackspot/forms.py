from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class review_form(forms.Form):
	review = forms.CharField(help_text = "Description:", max_length = 500)
	rating = forms.PositiveIntegerField(help_text = "Rating:", validators=[MaxValueValidator(100)])
	user = forms.CharField(help_text = "Username:", on_delete=models.CASCADE)
    album = forms.CharField('Album', on_delete=models.CASCADE, null=True, blank=True)
    song = forms.CharField('Song', on_delete=models.CASCADE, null=True, blank=True)