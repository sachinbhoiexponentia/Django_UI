from django.urls import path
from .views import *

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
<<<<<<< HEAD
    path('api/Threshold_Login_Config_get_data/<int:pk>/', threshold_logic_config_detail_view, name='get_by_id'),
    path('api/Threshold_Login_Config_delete/<int:row_id>/', delete_data_by_id, name='delete_data_by_id'),
    path('api/Trigg_Thres_By_Business_data/<int:pk>/', Trigg_Thres_By_Business_view, name='get_by_id_Trigg_Thres_By_Business'),
    path('upload/<sheet_name>/', upload_to_s3, name='upload_to_s3')
=======
    path('api/Threshold_Logic_Config_get_data/<int:pk>/', threshold_logic_config_detail_view, name='get_by_id'),
    path('api/Threshold_Logic_Config_delete/<int:row_id>/', threshold_logic_config_delete_data_by_id, name='delete_data_by_id'),
    
    path('api/Channel_Task_Mapping_get_data/<int:pk>/', channel_task_mapping_detail_view, name='get_by_id'),
    path('api/Channel_Task_Mapping_delete/<int:row_id>/', channel_task_mapping_delete_data_by_id, name='delete_data_by_id'),
    

    path('upload/<sheet_name>/', upload_to_s3, name='upload_to_s3'),
>>>>>>> 21f2d9ee8948c6a6e41c5b5efab29d7a1245b116
]
