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
        return self.product.price

    price.fget.short_description = 'قیمت'

    @property
    def product_total_price(self):
        return self.quantity * self.product.price

    product_total_price.fget.short_description = 'مجموع'

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'


class Order(models.Model):
    STATUS = (
        ('New', 'درحال بررسی'),
        ('Accepted', 'تایید شده'),
        ('Preparing', 'درحال آماده سازی'),
        ('OnShipping', 'ارسال شده'),
        ('Completed', 'تکمیل شده'),
        ('Canceled', 'لغو شده'),
        ('Referred', 'مرجوع شده'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    code = models.CharField(max_length=6, editable=False, verbose_name='شماره سفارش')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(blank=True, max_length=20, verbose_name='شماره تماس')
    address = models.CharField(blank=True, max_length=300, verbose_name='آدرس')
    state = models.CharField(blank=True, max_length=30, verbose_name='استان')
    city = models.CharField(blank=True, max_length=30, verbose_name='شهر')
    total = models.FloatField(verbose_name='مجموع')
    status = models.CharField(max_length=20, choices=STATUS, default='New', verbose_name='وضعیت سفارش')
    ip = models.CharField(blank=True, max_length=20)
    admin_note = models.CharField(blank=True, max_length=100, verbose_name='یادداشت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'درحال بررسی'),
        ('Accepted', 'تایید شده'),
        ('Canceled', 'لغو شده'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.IntegerField(verbose_name='تعداد')
    price = models.FloatField(verbose_name='قیمت')
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New', verbose_name='وضعیت سفارش')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
