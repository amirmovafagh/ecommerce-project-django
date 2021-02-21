from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE,
                            verbose_name='والد')
    title = models.CharField(max_length=50, unique=True, verbose_name='دسته بندی')
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    image = models.ImageField(blank=True, upload_to='images/', verbose_name='تصویر')
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    slug = models.SlugField(allow_unicode=True, unique=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

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

    class Meta:
        verbose_name = 'دسته\u200cبندی'
        verbose_name_plural = 'دسته\u200cبندی\u200cها'


class Product(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='دسته بندی')  # many to one with Category
    title = models.CharField(max_length=50, verbose_name='نام محصول')
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/', verbose_name='تصویر اصلی')
    price = models.IntegerField(verbose_name='قیمت')
    amount = models.IntegerField(verbose_name='موجودی')
    minamount = models.IntegerField(verbose_name='حداقل موجودی')
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

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات مرتبط با محصولات'
