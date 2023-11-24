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
    path('upload/<sheet_name>/', upload_to_s3, name='upload_to_s3'),
    
    
    path('TNT_Module_View/api/Channel_Task_Mapping_get_data/<int:pk>/', channel_task_mapping_detail_view, name='get_by_id'),
    path('TNT_Module_View/api/Channel_Task_Mapping_delete/<int:row_id>/', channel_task_mapping_delete_data_by_id, name='delete_data_by_id'),
    
    path('TNT_Module_View/api/task_trigger_mapping_get_data/<str:task_id>/', task_trigger_mapping_detail_view, name='task_trigger_mapping_detail_view'),
    path('TNT_Module_View/api/task_trigger_mapping_delete/<str:task_id>/', task_trigger_mapping_delete_data_by_id, name='task_trigger_mapping_delete_data_by_id'),
        
    path('TNT_Module_View/api/trigger_on_query_logic_get_data/<str:Trigger_id>/', trigger_on_query_detail_view, name='trigger_on_query_logic_detail_view'),
    path('TNT_Module_View/api/trigger_on_query_logic_delete/<str:Trigger_id>/', trigger_on_query_delete_data_by_id, name='trigger_on_query_logic_delete_data_by_id'),
        
    path('TOAM_Module_View/api/microsegment_default_tasks_get_data/<str:mdt_pk_id>/', microsegment_default_tasks_detail_view, name='microsegment_default_tasks__detail_view'),
    path('TOAM_Module_View/api/microsegment_default_tasks_delete/<str:mdt_pk_id>/', microsegment_default_tasks_delete_data_by_id, name='microsegment_default_tasks__delete_data_by_id'),
        

    
]
