from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('barbers/', views.barber_list, name='barbers'),
    path('barbers/<int:id>/', views.barber, name='barber'),
    path('search/', views.search, name='search'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]