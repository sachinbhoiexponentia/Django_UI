from django.urls import path
from .views import validate_thresold_config_df_api

urlpatterns = [
    path('api/validate_thresold_config_df/', validate_thresold_config_df_api, name='validate_config'),
    
]
