# Generated by Django 3.1.6 on 2021-05-05 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20210429_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-create_at', 'status'], 'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات'},
        ),
    ]
