# Generated by Django 4.2.2 on 2023-07-29 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0022_barbertimeslotavailability_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero', models.CharField(help_text='ANTRASTE', max_length=100, verbose_name='Antraste')),
                ('content', models.TextField(help_text='TURINYS', max_length=500, verbose_name='Turinys')),
                ('photo', models.ImageField(default='posts_pics/default.png', upload_to='posts_pics')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.barber')),
            ],
        ),
    ]
