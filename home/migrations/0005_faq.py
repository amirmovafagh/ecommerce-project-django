# Generated by Django 3.1.6 on 2021-02-21 14:10

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20201211_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_number', models.IntegerField()),
                ('question', models.CharField(max_length=300, verbose_name='سوال')),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='پاسخ')),
                ('status', models.CharField(choices=[('True', 'فعال'), ('False', 'غیرغعال')], max_length=20, verbose_name='وضعیت')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
            ],
        ),
    ]
