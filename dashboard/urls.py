from django.urls import path
from . import views

urlpatterns = [
    path('', views.Threshold_Login_Config_view, name='Threshold_login_config'),
    path('TNT_Module_view/', views.TNT_Module_view, name='TNT_module'),
]
