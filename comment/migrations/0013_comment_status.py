# Generated by Django 3.1.6 on 2021-04-25 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0012_auto_20210421_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.BooleanField(default=False, verbose_name='وضعیت'),
        ),
    ]
