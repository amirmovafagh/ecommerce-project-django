from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='نام کاربری:')
    email = forms.EmailField(max_length=200, label='ایمیل:')
    first_name = forms.CharField(max_length=100, label='نام:', )
    last_name = forms.CharField(max_length=100, label='نام خانوادگی:')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class EditProfileInfoForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','phone', 'address', 'city', 'state', 'postal_code', 'image']


class EditUserInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',]
