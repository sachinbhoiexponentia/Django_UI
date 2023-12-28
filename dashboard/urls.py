from django.urls import path
from . import views

urlpatterns = [
    path('', views.Threshold_Logic_Config_view, name='Threshold_Logic_Config_View'),
    path('product_cat_conf/', views.Product_Category_Config_view, name='Product_Category_Config_View'),
    path('closure_Config_view/', views.closure_Config_view, name='closure_dashboard'),
    path('TNT_Module_View/', views.TNT_Module_View, name='TNT_Module_View'),
    path('TOAM_Module_View/', views.TOAM_Module_View, name='TOAM_Module_View'),
    
    path('Threshold_form_success/', views.Threshold_form_success, name='Threshold_form_success'),
    path('Closure_form_success/', views.Closure_form_success, name='Closure_form_success'),
    path('TNT_form_success/', views.TNT_form_success, name='TNT_form_success'),
    path('TOAM_form_success/', views.TOAM_form_success, name='TOAM_form_success'),

    path('download_csv/', views.download_csv, name='download_csv'),    

]
