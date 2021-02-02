from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from product.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    quantity = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    price.fget.short_description = 'قیمت'

    @property
    def amount(self):
        return self.quantity * self.product.price

    amount.fget.short_description = 'مجموع'

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'
