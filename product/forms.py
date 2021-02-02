from django import forms
from django.core import validators

# class ContactForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی'}), label='', )
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'ایمیل'}), label='')
#     subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'موضوع'}), label='')
#     message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'متن پیام'}))
#     botcatcher = forms.CharField(required=False,
#                                  widget=forms.HiddenInput,
#                                  validators=[validators.MaxLengthValidator(0)])
from django.forms import ModelForm, TextInput, Textarea

from product.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'subject', 'rate', ]

    # labels = {
    #     'comment': "",
    #     'subject': "",
    #     'rate': "",
    # }
    #
    # widgets = {
    #     'name': TextInput(attrs={'class': 'input', 'placeholder': 'نام و نام خانوادگی'}),
    #     'subject': TextInput(attrs={'class': 'input', 'placeholder': 'موضوع'}),
    #     'email': TextInput(attrs={'class': 'input', 'placeholder': 'ایمیل'}),
    #     'message': Textarea(attrs={'class': 'input', 'placeholder': 'پیام شما...', 'row': '5'}),
    # }
