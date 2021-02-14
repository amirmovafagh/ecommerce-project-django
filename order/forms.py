from django.forms import ModelForm

from order.models import ShopCart, Order


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = []
