# Generated by Django 3.1.3 on 2020-11-18 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Gallery',
        ),
    ]
