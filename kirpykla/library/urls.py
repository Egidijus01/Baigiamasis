from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('barbers/', views.barber_list, name='barbers'),
    path('barbers/<int:id>/', views.barber, name='barber'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('settings/', views.map_settings, name='settings'),
    path('map/',views.map, name="map"),
    path('mydata',views.mydata, name="mydata"),
    path('profile/', views.profile, name='profile'),
    path('myorders/', views.LoanedOrdersByUserListView.as_view(), name='my-borrowed'),
    path('myorders/<int:pk>', views.OrderByUserDetailView.as_view(), name='my-book'),
    path('barbers/<int:id>/booking/', views.booking, name='booking'),
    path('barbers/<int:id>/booking/booking-submit/', views.bookingSubmit, name='bookingSubmit'),
    path("chat/" , views.chat),
    path('chat/<str:room_name>/', views.room, name='room'),
    # path('myorders/new', views.OrderByUserCreateView.as_view(), name='my-borrowed-new'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]