from django import forms
from reviews.models import *

class BusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		exclude = ('user',)