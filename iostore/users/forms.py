from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Address, User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class my_user_creation_form(UserCreationForm):

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        api_params={'hl': 'en'}
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        exclude = ['captcha']


class update_user_form(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'bio', 'avatar', 'is_dark_mode']

class  update_address_form(ModelForm):
    address = forms.CharField(max_length=250, required=True, widget = forms.HiddenInput())
    longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
    latitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())

    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['user']


class user_login_form(forms.Form):

    username = UsernameField(widget=forms.TextInput(
        attrs={
            "autofocus": True,
            "placeholder": 'Enter username'
        }))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "placeholder": 'Enter password'}),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        api_params={'hl': 'en'}
    ))

    class Meta:
        model = User
        fields = ['username, password']
