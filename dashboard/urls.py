from django.urls import path
from . import views

urlpatterns = [
    path('', views.Threshold_Logic_Config_view, name='Threshold_Logic_Config_View'),
    path('closure_Config_view/', views.closure_Config_view, name='closure_dashboard'),
    path('TNT_Module_View/', views.TNT_Module_View, name='TNT_Module_View'),
    path('TOAM_Module_View/', views.TOAM_Module_View, name='TOAM_Module_View'),

]
