# Generated by Django 3.1.6 on 2021-03-09 10:35

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210308_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='customerservices',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='خدمات مشتریان'),
        ),
        migrations.AddField(
            model_name='setting',
            name='worktime',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='ساعت کاری'),
        ),
    ]
