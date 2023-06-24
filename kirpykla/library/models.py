import uuid
from datetime import datetime

from django.db import models

# Create your models here.

class Rating(models.Model):
    RATING_CHOICES = (
        ("-", "-"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),

    )
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default="-")

    def __str__(self):
        return self.rating


class Barber(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4(), help_text='Unikalus kirpejo kodas')
    name = models.CharField('Vardas', max_length=50, help_text='Kirpejo vardas')
    last_name = models.CharField('Pavarde', max_length=50, help_text='Kirpejo pavarde')
    email = models.EmailField('Elektroninis pastas')
    about = models.TextField('Apie', max_length=200, help_text='Apie kirpeja')
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True)
    login_name = models.CharField('Prisijungimo vardas', max_length=20)
    # password =

    def __str__(self):
        return f'{self.name} {self.last_name}'


class User(models.Model):
    name = models.CharField('Vardas', max_length=50, help_text='Naudotojo vardas')
    last_name = models.CharField('Pavarde', max_length=50, help_text='Naudotojo pavarde')
    email = models.EmailField('Elektroninis pastas')
    login_name = models.CharField('Prisijungimo vardas', max_length=20)
    # password =

    def __str__(self):
        return f'{self.name} {self.last_name}'



class Messages(models.Model):
    pass

class Services(models.Model):
    service_name = models.CharField('Paslauga', max_length=100, help_text='Teikiama paslauga')
    price = models.FloatField('Paslaugos kaina')

    def __str__(self):
        return f'{self.service_name} {self.price}'

class Available_times(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    barber = models.ForeignKey(Barber, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ManyToManyField(Services)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)

    # def __str__(self):
    #     return f"{self.user.login_name}| {self.barber.login_name} | day: {self.day} | time: {self.time}"
