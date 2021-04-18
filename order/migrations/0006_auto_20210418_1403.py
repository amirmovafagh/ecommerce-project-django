# Generated by Django 3.1.6 on 2021-04-18 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_shipment_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shipment',
            options={'verbose_name': 'آیتم حمل و نقل', 'verbose_name_plural': 'حمل و نقل'},
        ),
        migrations.AddField(
            model_name='order',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.shipment', verbose_name='حمل و نقل'),
        ),
    ]
