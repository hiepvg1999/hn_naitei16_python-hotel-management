from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('user-profile/', views.UserProfileView.as_view(), name= 'user-profile'),
    path('edit_profile/', views.edit_profile, name = 'edit-profile'),
    path('list-users/', views.list_users, name = 'list-users'),
]
