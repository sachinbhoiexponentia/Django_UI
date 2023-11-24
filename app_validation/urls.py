from django.urls import path
from .views import *

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
    path('api/Threshold_Logic_Config_get_data/<int:pk>/', threshold_logic_config_detail_view, name='threshold_logic_config_detail_view'),
    path('api/Threshold_Logic_Config_delete/<int:row_id>/', threshold_logic_config_delete_data_by_id, name='threshold_logic_config_delete_data_by_id'),
    path('api/Trigg_Thres_By_Business_view/<int:pk>/', Trigg_Thres_By_Business_view, name='Trigg_Thres_By_Business_view'),
    path('api/Trigg_Thres_By_Business_delete/<int:row_id>/', Trigg_Thres_By_Business_delete_data_by_id, name='Trigg_Thres_By_Business_delete_data_by_id'),
    path('api/Channel_Task_Mapping_get_data/<int:pk>/', channel_task_mapping_detail_view, name='channel_task_mapping_detail_view'),
    path('api/Channel_Task_Mapping_delete/<int:row_id>/', channel_task_mapping_delete_data_by_id, name='channel_task_mapping_delete_data_by_id'),
    path('api/Default_Channel_Trigg_thres_data/<int:pk>/', Default_Channel_Trigg_thres_view, name='Default_Channel_Trigg_thres_view'),
    path('api/Default_Channel_Trigg_thres_delete/<int:row_id>/', Default_Channel_Trigg_thres_delete_data_by_id, name='Default_Channel_Trigg_thres_delete_data_by_id'),
    path('upload/<sheet_name>/', upload_to_s3, name='upload_to_s3')
]
