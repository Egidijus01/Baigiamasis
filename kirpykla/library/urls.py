from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('barbers/', views.barber_list, name='barbers'),
    path('barbers/<int:id>/', views.barber, name='barber'),
]