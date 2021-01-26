from django import forms
from django.core import validators


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی'}), label='', )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'ایمیل'}), label='')
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'موضوع'}), label='')
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'متن پیام'}))
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])

    # class Meta:
    #
    #     model = ContactMessage
    #     fields = ['name', 'email', 'subject', 'message']
    #
    #     error_messages = {
    #         'name': {
    #             'required': "This is a custom error message from modelform meta",
    #         },
    #     }
    #     labels = {
    #         'name': "",
    #         'email': "",
    #         'subject': "",
    #         'message': "",
    #     }
    #
    #     widgets = {
    #         'name': TextInput(attrs={'class': 'input', 'placeholder': 'نام و نام خانوادگی'}),
    #         'subject': TextInput(attrs={'class': 'input', 'placeholder': 'موضوع'}),
    #         'email': TextInput(attrs={'class': 'input', 'placeholder': 'ایمیل'}),
    #         'message': Textarea(attrs={'class': 'input', 'placeholder': 'پیام شما...', 'row': '5'}),
    #     }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()
