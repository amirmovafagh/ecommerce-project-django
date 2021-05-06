# Generated by Django 3.1.6 on 2021-05-03 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210427_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='توضیحات')),
                ('image', models.ImageField(help_text='حداقل نسبت تصویر قابل قبول 400 * 1500', upload_to='images/', verbose_name='تصویر')),
                ('status', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('page_url', models.URLField(verbose_name='آدرس')),
                ('ordering_position', models.IntegerField(verbose_name='ترتیب نمایش اسلاید')),
            ],
            options={
                'verbose_name': 'اسلاید',
                'verbose_name_plural': 'اسلایدر',
            },
        ),
    ]