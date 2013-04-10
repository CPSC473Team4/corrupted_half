from django import forms
from django.contrib.auth.forms import UserCreationForm
from reviews.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

# Needs to set form enctype="multipart/form-data" and assign user_id
class BusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		exclude = ('user', 'address_lat', 'address_lon')

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.method = 'post'
        self.helper.form_action = 'user_add'
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Fieldset(
                'Sign Up',
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        super(UserCreateForm, self).__init__(*args, **kwargs)
