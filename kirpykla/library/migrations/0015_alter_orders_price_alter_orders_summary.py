# Generated by Django 4.2.2 on 2023-07-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_remove_orders_service_orders_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Paslaugos kaina'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='summary',
            field=models.CharField(default='', max_length=200, verbose_name='Aprasymas'),
            preserve_default=False,
        ),
    ]