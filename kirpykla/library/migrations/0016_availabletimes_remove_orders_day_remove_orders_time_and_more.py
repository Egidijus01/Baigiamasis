# Generated by Django 4.2.2 on 2023-07-13 17:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_alter_orders_price_alter_orders_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default=datetime.datetime.now)),
                ('time', models.CharField(choices=[('3 PM', '3 PM'), ('3:30 PM', '3:30 PM'), ('4 PM', '4 PM'), ('4:30 PM', '4:30 PM'), ('5 PM', '5 PM'), ('5:30 PM', '5:30 PM'), ('6 PM', '6 PM'), ('6:30 PM', '6:30 PM'), ('7 PM', '7 PM'), ('7:30 PM', '7:30 PM')], default='3 PM', max_length=10)),
                ('status', models.CharField(blank=True, choices=[('g', 'galima'), ('n', 'negalima')], default='a', help_text='Statusas', max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='orders',
            name='day',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='time',
        ),
        migrations.AddField(
            model_name='barber',
            name='times',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.availabletimes'),
        ),
    ]
