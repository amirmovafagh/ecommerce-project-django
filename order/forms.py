from django.forms import ModelForm

from order.models import ShopCart


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
