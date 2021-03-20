from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, TextInput, EmailInput, FileInput

from user.models import UserProfile, UserAddress, User


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='نام کاربری:')
    email = forms.EmailField(max_length=200, label='ایمیل:')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class EditProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['vip_user'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'vip_user']

        """or we can used widgets method for change attribute of fields"""
        # widgets = {
        #     'username': TextInput(attrs={'class':  'input', 'disabled':'true','placeholder': 'شماره تماس'}),
        # }


class UpdateAddressForm(ModelForm):
    class Meta:
        model = UserAddress
        fields = ('firstname', 'lastname', 'phone', 'address', 'city', 'state', 'postalcode',)


# class UserUpdateForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', ]
#         widgets = {
#             'username': TextInput(attrs={'class': 'input', 'placeholder': 'نام کاربری'}),
#             'email': EmailInput(attrs={'class': 'input', 'placeholder': 'ایمیل'}),
#             'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'نام'}),
#             'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'نام خانوادگی'}),
#         }


# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
