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
    path('mydataall', views.mydata_all, name='mydata_all'),
    path('mydata/<int:pk>',views.mydata, name="mydata"),
    path('profile/', views.profile, name='profile'),
    path('myorders/', views.loaned_orders_by_user_list_view, name='my-borrowed'),
    path('myorders/<int:pk>', views.order_by_user_detail_view, name='my-book'),
    path('barbers/<int:id>/booking/', views.booking, name='booking'),
    path('barbers/<int:id>/booking/booking-submit/', views.bookingSubmit, name='bookingSubmit'),
    # path("chat/" , views.chat),
    # path('chat/<str:room_name>/', views.room, name='room'),
    path('chat/', views.chat_room_list, name='chat_room_list'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('becomebarber', views.become_barber, name='become_barber'),
    path('my-posts/<int:id>', views.my_posts, name='my_posts'),
    path('my-posts/<int:id>/create/', views.create_post, name='create_post'),
    path('my-posts/<int:id>/update/', views.update_post, name='update_post'),
    path('my-posts/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('explore', views.explore, name='explore'),
    path('get_paginated_data/', views.get_paginated_data, name='get_paginated_data'),
    path('barberorders/', views.loaned_orders_for_barber, name='barber-orders'),
    path('myorders/<int:pk>', views.order_by_user_detail_view_for_barber, name='barber-order'),




    # path('get_paginated_data_barbers/', views.get_paginated_data_barbers, name='get_paginated_data_barbers'),




  
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]