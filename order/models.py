from datetime import timedelta

from django.db import models

# Create your models here.
from django.utils import timezone

from extensions.utils import jalali_converter
from product.models import Product, Variants
from user.models import User


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True,
                                null=True)  # relation with variants table
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

    @property
    def product_variant_total_price(self):
        return self.quantity * self.variant.price

    product_total_price.fget.short_description = 'مجموع'

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید تکمیل نشده'


class Shipment(models.Model):
    title = models.CharField(max_length=40, verbose_name="نام")
    description = models.CharField(max_length=300, verbose_name="توضیحات")
    status = models.BooleanField(default=True, verbose_name="فعال")
    price = models.IntegerField(verbose_name='هزینه ارسال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'آیتم حمل و نقل'
        verbose_name_plural = 'حمل و نقل'


class Order(models.Model):
    STATUS = (
        ('OnPay', 'در انتظار پرداخت'),
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
    shipment = models.ForeignKey(Shipment, null=True, blank=True, verbose_name="حمل و نقل", on_delete=models.SET_NULL)
    total = models.IntegerField(verbose_name='مجموع')
    status = models.CharField(max_length=20, choices=STATUS, default='OnPay', verbose_name='وضعیت سفارش')
    postalcode = models.CharField(blank=True, max_length=20, verbose_name='کدپستی')
    ip = models.CharField(blank=True, max_length=20)
    admin_note = models.CharField(blank=True, max_length=100, verbose_name='یادداشت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')

    def is_order_pay_valid(self):
        if self.create_at + timedelta(days=1) > timezone.now():
            if self.status == "OnPay":
                return True
            else:
                return False
        else:
            if self.status == "OnPay":
                self.status = "Canceled"
                self.save()
            return False

    is_order_pay_valid.boolean = True  # show icon in list display
    is_order_pay_valid.short_description = "امکان پرداخت مجدد"

    def __str__(self):
        return self.user.first_name

    def status_persian(self):
        if self.status == 'OnPay':
            return 'در انتظار پرداخت'
        elif self.status == 'New':
            return 'درحال بررسی'
        elif self.status == 'Accepted':
            return 'تایید شده'
        elif self.status == 'Accepted':
            return 'تایید شده'
        elif self.status == 'Preparing':
            return 'درحال آماده سازی'
        elif self.status == 'OnShipping':
            return 'ارسال شده'
        elif self.status == 'Completed':
            return 'تکمیل شده'
        elif self.status == 'Canceled':
            return 'لغو شده'
        else:
            return 'مرجوع شده'

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ['-create_at', 'status']


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'درحال بررسی'),
        ('Accepted', 'تایید شده'),
        ('Canceled', 'لغو شده'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True)  # relation with varinat
    quantity = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت')
    amount = models.IntegerField(verbose_name='مجموع')
    status = models.CharField(max_length=20, choices=STATUS, default='New', verbose_name='وضعیت سفارش')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')

    def __str__(self):
        return self.product.title

    def status_persian(self):
        if self.status == 'New':
            return 'درحال بررسی'
        elif self.status == 'Accepted':
            return 'تایید شده'
        else:
            return 'لغو شده'

    class Meta:
        verbose_name = 'محصول فروخته شده'
        verbose_name_plural = 'محصولات فروخته شده'

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'
