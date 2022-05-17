from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
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