# Generated by Django 4.2.2 on 2023-06-20 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='kaina',
            new_name='price',
        ),
    ]
