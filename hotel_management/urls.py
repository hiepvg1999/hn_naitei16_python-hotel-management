"""hotel_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hotel.views import user_register, rooms, room_profile, room_edit, room_add

urlpatterns = [
    path('admin/', admin.site.urls),
    # urls for user
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_register , name = "register"),
    path('', include('hotel.urls')),
     # urls for room
    path('rooms/', rooms, name= 'rooms'),
    path('room-add/', room_add, name= 'room-add'),
    path('room-profile/<int:number>', room_profile, name= 'room-profile'),
    path('room-edit/<int:number>', room_edit, name='room-edit'),
]
