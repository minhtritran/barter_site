from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin.widgets import AdminDateWidget
from .models import User, Feedback, Favor, Offer, Agreement, Tag
from django.template.defaultfilters import slugify


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    date_of_birth = forms.DateField(label="Date Of Birth",
                                    widget=forms.TextInput(
                                        attrs={'autocomplete': 'off', 'placeholder': 'MM/DD/YYYY'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'gender')

    def clean(self):
        # run the standard clean method first
        cleaned_data = super(UserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # check if passwords are entered and match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        # always return the cleaned data
        return cleaned_data

    def clean_email(self):
        # check if email is a .edu email
        email_domain = self.cleaned_data['email'].split('.')[-1]
        if email_domain != 'edu':
            raise forms.ValidationError("You must register with an edu email address.")
        return self.cleaned_data['email']
    """
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    """
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender')

    # def clean(self):
    #     # run the standard clean method first
    #     cleaned_data = super(UserCreationForm, self).clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #
    #     # check if passwords are entered and match
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords do not match!")
    #
    #     # always return the cleaned data
    #     return cleaned_data
    '''
    def clean_email(self):
        # check if email is a .edu email
        email_domain = self.cleaned_data['email'].split('.')[-1]
        if email_domain != 'edu':
            raise forms.ValidationError("You must register with an edu email address.")
        return self.cleaned_data['email']
    '''
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PasswordForm(forms.Form):
    password = forms.CharField(label='Current Password', widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        if not self.user.check_password(self.cleaned_data['password']):
            raise ValidationError('Wrong current password.')

        return self.cleaned_data['password']

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        new_password = cleaned_data['password1']
        retyped_password = cleaned_data['password2']

        if len(new_password) == 0 or len(retyped_password) == 0:
            raise ValidationError('Blank password fields.')

        if new_password != retyped_password:
            raise ValidationError('New password and retyped password do not match.')

        return cleaned_data


class FavorForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": 'off'}))
    tags = forms.CharField(label='Tags', widget=forms.HiddenInput, required=True)

    class Meta:
        model = Favor
        fields = ['title', 'message']

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     tags = cleaned_data.get('tags').split(',')
    #     for tag in tags:
    #         print("tag: " + tag)
    #         print("slugify(tag): " + slugify(tag))
    #         print("slugify(tag).strip(): " + slugify(tag).strip())
    #         if not slugify(tag).strip():
    #             raise ValidationError('Invalid tag.')
    #
    #     return cleaned_data

    # def clean_tags(self):
    #     tags = self.cleaned_data['tags']
    #     if tags is '':
    #         raise ValidationError("The tag field is empty.")

    def save(self, commit=True):
        favor = super(FavorForm, self).save(commit=False)
        if commit:
            favor.save()
        return favor


class FavorEditForm(forms.ModelForm):
    class Meta:
        model = Favor
        fields = ('title', 'message')

    def clean_title(self):
        if not self.cleaned_data['title'].strip():
            raise ValidationError('Blank title field.')
        return self.cleaned_data['title']

    def clean_message(self):
        if not self.cleaned_data['message'].strip():
            raise ValidationError('Blank message field.')
        return self.cleaned_data['message']

    def clean(self):
        cleaned_data = super(FavorEditForm, self).clean()
        return cleaned_data


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['message']

    def save(self, commit=True):
        offer = super(OfferForm, self).save(commit=False)
        if commit:
            offer.save()
        return offer


class FeedbackForm(forms.ModelForm):
    rating = forms.DecimalField(label="Rating", widget=forms.HiddenInput)

    class Meta:
        model = Feedback
        fields = ['message']

    def save(self, commit=True):
        feedback = super(FeedbackForm, self).save(commit=False)
        if commit:
            feedback.save()
        return feedback