# Generated by Django 3.1.6 on 2021-04-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20210326_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producthit',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='variants',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='تعداد موجودی'),
        ),
    ]