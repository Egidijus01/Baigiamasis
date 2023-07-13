import uuid
from datetime import date, datetime
from django.contrib.auth.models import User
from PIL import Image
from django.db import models
from django.urls import reverse

# Create your models here.

class Rating(models.Model):
    barber = models.ForeignKey('Barber', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    RATING_CHOICES = (
        ("-", "-"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),

    )
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default="-")
    content = models.TextField('Atsiliepimas', max_length=2000, default='')
    
    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']
    

    def __str__(self):
        return self.rating


class Barber(models.Model):
    name = models.CharField('Vardas', max_length=50, help_text='Kirpejo vardas')
    last_name = models.CharField('Pavarde', max_length=50, help_text='Kirpejo pavarde')
    email = models.EmailField('Elektroninis pastas')
    about = models.TextField('Apie', max_length=200, help_text='Apie kirpeja')
    login_name = models.CharField('Prisijungimo vardas', max_length=20)
    zipcode = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    adress = models.CharField(max_length=200,blank=True, null=True)



    cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)
    def __str__(self):
        return f'{self.name} {self.last_name}'




class Messages(models.Model):
    pass



class Orders(models.Model):
    TIME_CHOICES = (
        ("3 PM", "3 PM"),
        ("3:30 PM", "3:30 PM"),
        ("4 PM", "4 PM"),
        ("4:30 PM", "4:30 PM"),
        ("5 PM", "5 PM"),
        ("5:30 PM", "5:30 PM"),
        ("6 PM", "6 PM"),
        ("6:30 PM", "6:30 PM"),
        ("7 PM", "7 PM"),
        ("7:30 PM", "7:30 PM"),
    )
    id = models.AutoField(primary_key=True)
    barber = models.ForeignKey(Barber, on_delete=models.SET_NULL, null=True, blank=True)
    service_name = models.CharField('Paslauga', max_length=100, help_text='Teikiama paslauga')
    summary = models.CharField('Aprasymas', max_length=200)
    price = models.FloatField('Paslaugos kaina', blank=True, null=True)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    booker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def is_overdue(self):
        if self.time_ordered and date.today() > self.time_ordered:
            return True
        return False

    def get_absolute_url(self):
        return reverse('barber', args=[str(self.id)]) 



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self) -> str:
        return f'{self.user.username} profilis'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)