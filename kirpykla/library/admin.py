from django.contrib import admin
from .models import Rating,Services,Available_times,Messages, Barber
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('barber', 'date_created', 'reviewer', 'rating', 'content')



admin.site.register(Rating, ReviewAdmin)
admin.site.register(Services)
admin.site.register(Available_times)
admin.site.register(Barber)
admin.site.register(Messages)
