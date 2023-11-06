from django.urls import path
from . import views
from django.shortcuts import render
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('', views.dashboard, name='dashboard'),
    # Add more URL patterns as needed
]
