from django.urls import path
from .views import *

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
    path('api/Threshold_Login_Config_get_data/<int:pk>/', threshold_login_config_detail_view, name='get_by_id'),
    path('api/Threshold_Login_Config_delete/<int:row_id>/', delete_data_by_id, name='delete_data_by_id'),
    path('TOAM_Module_View/api/optimization_rules_get_data/<int:pk>/', optimization_rules_detail_view, name='optimization_rules_detail_view'),
    path('TOAM_Module_View/api/optimization_rules_delete/<int:row_id>/', optimization_rules_delete_by_id, name='optimization_rules_delete_by_id')
    
]
