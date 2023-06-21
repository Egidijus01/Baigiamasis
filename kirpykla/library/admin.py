from django.contrib import admin
from .models import Rating,Services,User,Available_times,Messages, Barber
# Register your models here.
admin.site.register(Rating)
admin.site.register(Services)
admin.site.register(User)
admin.site.register(Available_times)
admin.site.register(Barber)
admin.site.register(Messages)
