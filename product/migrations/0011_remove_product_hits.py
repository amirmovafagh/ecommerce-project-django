# Generated by Django 3.1.6 on 2021-03-26 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20210325_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hits',
        ),
    ]
