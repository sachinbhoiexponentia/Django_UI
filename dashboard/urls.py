from django.urls import path
from . import views

urlpatterns = [
    path('', views.Threshold_Login_Config_view, name='dashboard'),
    path('closure_Config_view/', views.closure_Config_view, name='closure_dashboard')

]
