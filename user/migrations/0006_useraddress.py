# Generated by Django 3.1.6 on 2021-02-13 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0005_auto_20210211_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='نام خانوادگی')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='شماره تماس')),
                ('address', models.CharField(blank=True, max_length=300, verbose_name='آدرس')),
                ('city', models.CharField(blank=True, max_length=30, verbose_name='شهر')),
                ('state', models.CharField(blank=True, max_length=30, verbose_name='استان')),
                ('postal_code', models.IntegerField(blank=True, default=0, verbose_name='کدپستی')),
                ('default_shipping_address', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
    ]