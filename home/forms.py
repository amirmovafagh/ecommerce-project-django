from django import forms
from django.core import validators
from django.core.files.images import get_image_dimensions

from home.models import SliderContent


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


class SliderImageValidForm(forms.ModelForm):
    class Meta:
        model = SliderContent
        fields = ['description', 'image', 'status', 'page_url', 'ordering_position']

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("تصویری یافت نشد!")
        else:
            w, h = get_image_dimensions(image)
            if w / h > 1.9:
                return image
            if w < 1500:
                raise forms.ValidationError("عرض تصویر %i px می باشد. حداقل عرض قابل قبول 1500px می باشد." % w)
            if h < 400:
                raise forms.ValidationError("ارتفاع تصویر %i px می باشد. حداقل ارتفاع قابل قبول 400px می باشد." % h)
        return image


class BannerImageValidForm(forms.ModelForm):
    class Meta:
        model = SliderContent
        fields = ['description', 'image', 'status', 'page_url', 'ordering_position']

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("تصویری یافت نشد!")
        else:
            w, h = get_image_dimensions(image)
            if h < 300:
                raise forms.ValidationError("ارتفاع تصویر %i px می باشد. حداکثر ارتفاع قابل قبول 300px می باشد." % h)
            if w < 600:
                raise forms.ValidationError("عرض تصویر %i px می باشد. حداکثر عرض قابل قبول 600px می باشد." % w)
        return image
