from django.urls import path
from . import views
from django.shortcuts import render
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('', views.dashboard, name='dashboard'),
    # Add more URL patterns as needed
]
