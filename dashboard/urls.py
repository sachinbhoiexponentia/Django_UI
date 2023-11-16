from django.urls import path
from . import views

urlpatterns = [
    path('', views.Threshold_Login_Config_view, name='dashboard'),
]
