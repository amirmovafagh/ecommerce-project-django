# Generated by Django 3.1.6 on 2021-04-21 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0011_follower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-posted'], 'verbose_name': 'نظر', 'verbose_name_plural': 'نظرها'},
        ),
        migrations.AlterModelOptions(
            name='flag',
            options={'verbose_name': 'فلگ', 'verbose_name_plural': 'فلگ ها'},
        ),
        migrations.AlterModelOptions(
            name='follower',
            options={'verbose_name': 'دنبال کننده', 'verbose_name_plural': 'دنبال کننده ها'},
        ),
        migrations.AlterModelOptions(
            name='reaction',
            options={'verbose_name': 'بازخورد', 'verbose_name_plural': 'بازخوردها'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='نظر'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='edited',
            field=models.DateTimeField(auto_now=True, verbose_name='زمان تغییر'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.comment', verbose_name='والد'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='posted',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='زمان ارسال'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='username',
            field=models.CharField(max_length=50, verbose_name='نام کاربری'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='comment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comment.comment', verbose_name='دیدگاه'),
        ),
    ]
