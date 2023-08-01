import uuid
from datetime import date, datetime
from django.contrib.auth.models import User, Group
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
   

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField('Vardas', max_length=50)
    last_name = models.CharField('Pavardė', max_length=50)
    email = models.EmailField('Elektroninis paštas')
    about = models.TextField('Apie', max_length=200)
    login_name = models.CharField('Prisijungimo vardas', max_length=20)
    zipcode = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    adress = models.CharField(max_length=200,blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)


    cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)
    def __str__(self):
        return f'{self.name} {self.last_name}'

    def resize_cover_image(self):
        if not self.cover:
            return

        max_size = (300, 300)  # Set the maximum size for the image (width, height)

        with Image.open(self.cover.path) as img:
            img.thumbnail(max_size, Image.ANTIALIAS)
            img.save(self.cover.path)


class Posts(models.Model):
    hero = models.CharField('Antraste', max_length=100, help_text="ANTRASTE")
    content = models.TextField('Turinys', max_length=500, help_text='TURINYS')
    photo = models.ImageField(default='posts_pics/default.png', upload_to='posts_pics')
    author = models.ForeignKey(Barber, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)



class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)



class Orders(models.Model):

    id = models.AutoField(primary_key=True)
    barber = models.ForeignKey(Barber, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.CharField('Paslauga', max_length=100, help_text='Teikiama paslauga')
    summary = models.CharField('Aprasymas', max_length=200)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    price = models.FloatField('Paslaugos kaina', blank=True, null=True)
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    booker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.day} - {self.time}    {self.barber}"

    def is_overdue(self):
        if self.time_ordered and date.today() > self.time_ordered: # type: ignore
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

class BarberTimeSlotAvailability(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    day = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['barber', 'day', 'time']

    def __str__(self):
        return f"{self.barber} - {self.day} - {self.time}"
