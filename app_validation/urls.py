from django.urls import path
from .views import *

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
    path('api/Threshold_Login_Config_get_data/<int:pk>/', threshold_login_config_detail_view, name='get_by_id'),
    path('api/Threshold_Login_Config_delete/<int:row_id>/', delete_data_by_id, name='delete_data_by_id'),
    path('api/Trigg_Thres_By_Business_data/<int:pk>/', Trigg_Thres_By_Business_view, name='get_by_id_Trigg_Thres_By_Business')
    
]
