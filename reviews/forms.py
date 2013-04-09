from django import forms
from django.contrib.auth.forms import UserCreationForm
from reviews.models import *

class BusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		exclude = ('user',)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #userName = forms.userName(required=True)

    class Meta:
        model = User
        fields = ( "username", "email" )


    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            return redirect("somewhere")
        return render(request,
                      self.template_name,
                      { 'user_form' : user_form })
