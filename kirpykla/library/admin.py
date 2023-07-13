from django.contrib import admin
from .models import Rating,Orders,Messages, Barber, Profile
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('barber', 'date_created', 'reviewer', 'rating', 'content')



admin.site.register(Rating, ReviewAdmin)

admin.site.register(Orders)
admin.site.register(Barber)
admin.site.register(Messages)
admin.site.register(Profile)
