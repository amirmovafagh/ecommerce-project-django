# Generated by Django 3.1.4 on 2021-01-27 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات مرتبط با محصولات'},
        ),
    ]
