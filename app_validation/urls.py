from django.urls import path
from .views import *

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
    path('api/Threshold_Logic_Config_get_data/<int:pk>/', threshold_logic_config_detail_view, name='get_by_id'),
    path('api/Threshold_Logic_Config_delete/<int:row_id>/', threshold_logic_config_delete_data_by_id, name='delete_data_by_id'),
    path('TOAM_Module_View/api/task_constraint_rules_get_data/<int:pk>/', task_constraint_rules_detail_view, name='task_constraint_rules_detail_view'),
    path('TOAM_Module_View/api/task_constraint_rules_delete/<int:row_id>/', task_constraint_rules_delete_by_id, name='optimization_rules_delete_by_id'),
    path('api/Channel_Task_Mapping_get_data/<int:pk>/', channel_task_mapping_detail_view, name='get_by_id'),
    path('api/Channel_Task_Mapping_delete/<int:row_id>/', channel_task_mapping_delete_data_by_id, name='delete_data_by_id'),
    path('upload/<sheet_name>/', upload_to_s3, name='upload_to_s3'),
]
