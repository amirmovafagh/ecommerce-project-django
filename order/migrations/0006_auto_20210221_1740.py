# Generated by Django 3.1.6 on 2021-02-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210219_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='amount',
            field=models.IntegerField(verbose_name='مجموع'),
        ),
    ]