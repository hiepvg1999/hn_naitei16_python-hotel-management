from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('user-profile/', views.UserProfileView.as_view(), name= 'user-profile'),
    path('edit_profile/', views.edit_profile, name = 'edit-profile'),
    path('list-users/', views.list_users, name = 'list-users'),
    path('list-bookings/', views.list_bookings_staff, name = "list-bookings-staff"),
    path('statistic_page/', views.statistic_page, name = 'statistic_page'),
    path('payment/<uuid:booking_id>', views.payment, name= 'payment')
]
