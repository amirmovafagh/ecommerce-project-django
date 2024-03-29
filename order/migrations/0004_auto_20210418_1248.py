# Generated by Django 3.1.6 on 2021-04-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210310_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='نام')),
                ('description', models.CharField(max_length=300, verbose_name='توضیحات')),
                ('price', models.IntegerField(verbose_name='هزینه ارسال')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('OnPay', 'در انتظار پرداخت'), ('New', 'درحال بررسی'), ('Accepted', 'تایید شده'), ('Preparing', 'درحال آماده سازی'), ('OnShipping', 'ارسال شده'), ('Completed', 'تکمیل شده'), ('Canceled', 'لغو شده'), ('Referred', 'مرجوع شده')], default='OnPay', max_length=20, verbose_name='وضعیت سفارش'),
        ),
    ]
