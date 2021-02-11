from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    phone = models.CharField(blank=True, max_length=20, verbose_name='شماره تماس')
    address = models.CharField(blank=True, max_length=300, verbose_name='آدرس')
    city = models.CharField(blank=True, max_length=30, verbose_name='شهر')
    state = models.CharField(blank=True, max_length=30, verbose_name='استان')
    postal_code = models.IntegerField(blank=True, verbose_name='کدپستی', default=0)
    image = models.ImageField(blank=True, upload_to='images/users/', verbose_name='تصویر')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    user_name.short_description = 'نام کاربری'

    def image_tag(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe('<img src="{}" height="40"/>'.format(self.image.url))
        else:
            return mark_safe('<img src="/static/images/user.png" height="40"/>')

    image_tag.short_description = 'تصویر پروفایل'
    image_tag.allow_tags = True

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
