from django.contrib.auth.forms import UserCreationForm
from django import forms
from barter.models import User


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='30 characters max.')
    last_name = forms.CharField(max_length=30, help_text='30 characters max.')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user