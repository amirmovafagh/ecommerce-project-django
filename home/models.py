from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

from extensions.utils import jalali_converter


class Setting(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )
    title = models.CharField(max_length=150, verbose_name='عنوان وب سایت')
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, verbose_name='عنوان')
    company = models.CharField(blank=True, max_length=50, verbose_name='شرکت')
    address = models.CharField(blank=True, max_length=255, verbose_name='آدرس')
    phone = models.CharField(blank=True, max_length=20,
                             verbose_name="تلفن همراه (جهت دریافت اطلاع رسانی پیامکی وبسایت)")
    phone2 = models.CharField(blank=True, max_length=20, verbose_name='شماره تماس ثابت')
    fax = models.CharField(blank=True, max_length=20, verbose_name='فکس')
    email = models.CharField(blank=True, max_length=70, verbose_name='ایمیل')
    # smtpserver = models.CharField(blank=True, max_length=20)
    # smtpemail = models.CharField(blank=True, max_length=50)
    # smtppassword = models.CharField(blank=True, max_length=50)
    # smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/', verbose_name='لوگو')
    facecbook = models.CharField(blank=True, max_length=50, verbose_name='فیسبوک')
    instagram = models.CharField(blank=True, max_length=50, verbose_name='اینستاگرام')
    telegram = models.CharField(blank=True, max_length=50, verbose_name='تلگرام')
    youtube = models.CharField(blank=True, max_length=50, verbose_name='یوتیوب')
    twitter = models.CharField(blank=True, max_length=50, verbose_name='توییتر')
    aboutus = RichTextUploadingField(blank=True, verbose_name='درباره ما')
    contact = RichTextUploadingField(blank=True, verbose_name='تماس با ما')
    worktime = RichTextUploadingField(blank=True, verbose_name='ساعت کاری')
    customerservices = RichTextUploadingField(blank=True, verbose_name='خدمات مشتریان')
    notices = RichTextUploadingField(blank=True, verbose_name="اعلامیه وبسایت")
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __String__(self):
        return self.title

    class Meta:
        verbose_name = 'اطلاعات وب سایت'
        verbose_name_plural = 'اطلاعات سایت'

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'


class SliderManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class SliderContent(models.Model):
    description = models.CharField(blank=True, max_length=255, verbose_name="توضیحات")
    image = models.ImageField(upload_to='images/', verbose_name="تصویر",
                              help_text="حداقل نسبت تصویر 2:1 می باشد - رزولوشن قابل قبول 400 * 1500")
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    page_url = models.URLField(max_length=200, verbose_name="آدرس")
    ordering_position = models.IntegerField(verbose_name="ترتیب نمایش اسلاید")

    objects = SliderManager()

    def __str__(self):
        return self.description

    def image_tag(self):
        return mark_safe('<img style="border-radius: 5px" src="{}" height="75"/>'.format(self.image.url))

    image_tag.short_description = "تصویر"

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدر'
        ordering = ["ordering_position"]


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Read', 'خوانده شده'),
        ('Closed', 'بسته'),
    )
    name = models.CharField(max_length=30, blank=True, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=70, verbose_name='ایمیل')
    subject = models.CharField(max_length=50, verbose_name='موضوع')
    message = models.CharField(max_length=255, verbose_name='پیام')
    note = models.CharField(blank=True, max_length=255, verbose_name='پاسخ')
    ip = models.CharField(blank=True, max_length=20, verbose_name='آی پی')
    status = models.CharField(max_length=30, choices=STATUS, default='New', verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'


class BannerManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class BannerContent(models.Model):
    description = models.CharField(max_length=255, verbose_name="توضیحات")
    image = models.ImageField(upload_to='images/', verbose_name="تصویر اصلی",
                              help_text="این بنر در قسمت پایین صفحه اصلی سایت نمایش داده خواهد شد.")
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    page_url = models.URLField(max_length=200, verbose_name="آدرس")
    ordering_position = models.IntegerField(verbose_name="ترتیب نمایش بنر")

    objects = BannerManager()

    def __str__(self):
        return self.description

    def image_tag(self):
        return mark_safe('<img style="border-radius: 5px" src="{}" height="75"/>'.format(self.image.url))

    image_tag.short_description = "تصویر"

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
        ordering = ["ordering_position"]


class BrandManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class BrandContent(models.Model):
    description = models.CharField(max_length=255, verbose_name="توضیحات")
    logo = models.ImageField(upload_to='images/', verbose_name="تصویر")
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    page_url = models.URLField(max_length=200, verbose_name="آدرس")
    ordering_position = models.IntegerField(verbose_name="ترتیب نمایش برند")

    objects = BrandManager()

    def __str__(self):
        return self.description

    def image_tag(self):
        return mark_safe('<img style="border-radius: 5px" src="{}" height="75"/>'.format(self.logo.url))

    image_tag.short_description = "تصویر"

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
        ordering = ["ordering_position"]


class FAQ(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )
    ordering_number = models.IntegerField()
    question = models.CharField(max_length=300, verbose_name='سوال')
    answer = RichTextUploadingField(blank=True, verbose_name='پاسخ')
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات پر تکرار'
        ordering = ["ordering_number"]
