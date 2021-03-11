from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.db import models

# Create your models here.
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from extensions.utils import jalali_converter
from user.models import User


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL,
                            verbose_name='والد')
    title = models.CharField(max_length=50, unique=True, verbose_name='دسته بندی')
    keywords = models.CharField(max_length=255, blank=True, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, blank=True, verbose_name='توضیحات')
    image = models.ImageField(blank=True, upload_to='images/', verbose_name='تصویر')
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    slug = models.SlugField(allow_unicode=True, unique=True, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    class Meta:
        verbose_name = 'دسته\u200cبندی'
        verbose_name_plural = 'دسته\u200cبندی\u200cها'


class Product(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )

    VARIANTS = (
        ('None', 'ندارد'),
        ('Size', 'تنوع از نظر سایز'),
        ('Color', 'تنوع از نظر رنگ'),
        ('SizeColor', 'تنوع از نظر سایز و رنگ'),
    )
    category = models.ManyToManyField(Category,
                                      verbose_name='دسته بندی')  # many to many with Category
    title = models.CharField(max_length=50, verbose_name='نام محصول')
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/', verbose_name='تصویر اصلی')
    price = models.IntegerField(verbose_name='قیمت')
    amount = models.IntegerField(verbose_name='موجودی')
    minamount = models.IntegerField(verbose_name='حداقل موجودی')
    variant = models.CharField(max_length=20, choices=VARIANTS, default='None', verbose_name='تنوع محصول')
    detail = RichTextUploadingField(verbose_name='جزئیات')
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    slug = models.SlugField(allow_unicode=True, unique=True, null=False)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def average_review(self):
        reviews = Comment.objects.filter(product=self).aggregate(average=Avg('rate'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def counter_view(self):
        reviews = Comment.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    title = models.CharField(max_length=50, blank=True, verbose_name='نام')
    image = models.ImageField(blank=True, upload_to='images/', verbose_name='تصویر')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالری تصاویر'


class Comment(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('True', 'تایید'),
        ('False', 'عدم تایید'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    subject = models.CharField(max_length=50, verbose_name='موضوع')
    comment = models.CharField(max_length=350, verbose_name='نظر')
    rate = models.IntegerField(default=1)
    ip = models.CharField(blank=True, max_length=20, verbose_name='آی پی')
    status = models.CharField(max_length=20, choices=STATUS, default='New', verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.subject

    def status_persian(self):
        if self.status == 'True':
            return 'تایید'
        elif self.status == 'False':
            return 'عدم تایید'
        else:
            return 'جدید'

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات مرتبط با محصولات'


class Color(models.Model):
    name = models.CharField(max_length=25, verbose_name='رنگ')
    code = ColorField(default='#FF0000')

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">رنگ</p>'.format(self.code))
        else:
            return ""

    color_tag.short_description = 'رنگ'

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'


class Size(models.Model):
    name = models.CharField(max_length=25, verbose_name='سایز')
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name='کد سایز')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'اندازه_حجم'
        verbose_name_plural = 'اندازه و حجم ها'


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True, verbose_name='رنگ')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, verbose_name='سایز')
    image_id = models.IntegerField(blank=True, null=True, default=0, verbose_name='آی دی تصویر مورد نظر برای نمایش')
    quantity = models.IntegerField(default=1, verbose_name='تعداد موجودی')
    price = models.IntegerField(default=0, verbose_name='قیمت')

    def __str__(self):
        if self.title is None:
            return "بدون نام"
        return self.title

    def image_var(self):
        img = Gallery.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Gallery.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

    image_tag.short_description = 'تصویر'

    class Meta:
        verbose_name = 'نوع'
        verbose_name_plural = 'انواع'
