from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.


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
    phone = models.CharField(blank=True, max_length=20, verbose_name='شماره تماس')
    fax = models.CharField(blank=True, max_length=20, verbose_name='فکس')
    email = models.CharField(blank=True, max_length=70, verbose_name='ایمیل')
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=50)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/', verbose_name='لوگو')
    facecbook = models.CharField(blank=True, max_length=50, verbose_name='فیسبوک')
    instagram = models.CharField(blank=True, max_length=50, verbose_name='اینستاگرام')
    telegram = models.CharField(blank=True, max_length=50, verbose_name='تلگرام')
    youtube = models.CharField(blank=True, max_length=50, verbose_name='یوتیوب')
    twitter = models.CharField(blank=True, max_length=50, verbose_name='توییتر')
    aboutus = RichTextUploadingField(blank=True, verbose_name='درباره ما')
    contact = RichTextUploadingField(blank=True, verbose_name='تماس با ما')
    refrences = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __String__(self):
        return self.title

    class Meta:
        verbose_name = 'اطلاعات وب سایت'
        verbose_name_plural = 'اطلاعات سایت'


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Read', 'خوانده شده'),
        ('Closed', 'بسته'),
    )
    name = models.CharField(max_length=30, blank=True, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(blank=True, max_length=70, verbose_name='ایمیل')
    subject = models.CharField(blank=True, max_length=50, verbose_name='موضوع')
    message = models.CharField(blank=True, max_length=255, verbose_name='پیام')
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