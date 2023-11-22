from django.urls import path
from .views import validate_thresold_config_df_api

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
    # path('api/get_by_id/<int:pk>/', Threshold_Login_ConfigDetailView.as_view(), name='get_by_id')
    
]
