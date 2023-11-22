from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from app_validation.models import Threshold_Login_Config,Trigg_Thres_By_Business,Segment_Threshold_Output,FLS_Avg_Threshold_Output,Task_Closure_Config
from .controller import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
import pandas as pd

@csrf_exempt
@login_required 
def validate_thresold_config_df_api(request):
    print("validate_thresold_config_df_api function")
    if request.method == 'GET':
        print('GET Method')
        try:
            data = request.GET
            parameters = dict(data.lists())
            data_df = pd.DataFrame(parameters)
            print(data_df)
            sheet_name = request.GET.get('sheet') # to be checked
            print('sheet_name',sheet_name)
            is_valid,errors = mainValidate_function(sheet_name, data_df)
            return JsonResponse({'is_valid': is_valid, 'errors': errors})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# class Threshold_Login_ConfigDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             instance = Threshold_Login_Config.objects.get(pk=pk)
#         except Threshold_Login_Config.DoesNotExist:
#             return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        
#         return Response(data)




###################insert the config data into the model###################
# def insert_config_data(df):
#     print(df.columns)
#     for index, row in df.iterrows():
#         threshold_login_config = Threshold_Login_Config(
#             trigger_id=row['Trigger_id'],
#             trigg_desc=row['Trigg_Desc'],
#             thres_description=row['Thres_Description'],
#             thres_query_logic=row['Thres_Query_Logic'],
#             operation=row['Operation'],
#             analysis_period=row['Analysis_Period'],
#             num_thresholds_required=row['Num_thresholds_required'],
#             segment_threshold_requirement_flag=row['Segment_Threshold_Requirement_Flag'],
#             FLS_Threshold_Requirement_Flag=row['FLS_Threshold_Requirement_Flag'],
#         )
#         threshold_login_config.save()
# df = pd.read_excel('Config Template 081123.xlsx', sheet_name='1.a Threshold Logic Config',skiprows=1)
# insert_config_data(df)

###################CRED Operations#######################
# # Create
# threshold = Threshold_Login_Config(
#     trigger_id=1,
#     trigg_desc="If Last N month's avg TAT between lead generation and set up of meeting...",
#     # ... (other fields)
# )
# threshold.save()
# Read
# queryset = Threshold_Login_Config.objects.all()
# df = pd.DataFrame(list(queryset.values()))
# print(df.to_string(index=False))
# # Update
# threshold = Threshold_Login_Config.objects.get(trigger_id=1)
# threshold.trigg_desc = "Updated description"
# threshold.save()
# # Delete
# threshold = Threshold_Login_Config.objects.get(trigger_id=1)
# threshold.delete()
############################################################

###################insert the config data into the model###################
# def insert_config_data(df):
#     print(df.columns)
#     for index, row in df.iterrows():
#         trigg_Thres_By_Business = Trigg_Thres_By_Business(
#             Channel=row['Channel'],
#             Subchannel=row['Subchannel'],
#             Channel_Subchannel_ID=row['Channel_Sunchannel_ID'],
#             DemoSeg=row['DemoSeg'],
#             ValueSeg=row['ValueSeg'],
#             DemoSeg_ValueSeg_ID=row['DemoSeg_ValueSeg_ID'],
#             Trigger_id =row['Trigger_id'],
#             Trigg_Desc=row['Trigg_Desc'],
#             Segment_Threshold=row['Segment_Threshold'],
#             FLSAvg_Threshold=row['FLSAvg_Threshold']
#         )
#         trigg_Thres_By_Business.save()
# df = pd.read_excel('Config Template 081123.xlsx', sheet_name='1.b Trigg_Thres_by_Business',skiprows=1)
# insert_config_data(df)