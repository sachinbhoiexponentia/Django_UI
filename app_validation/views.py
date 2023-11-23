from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from app_validation.models import *
from django.apps import apps
from .controller import mainValidate_function,s3_upload
from .config import s3_bucket,s3_path
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
# from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
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
            if 'csrfmiddlewaretoken' in parameters:
                csrf_token = parameters.pop('csrfmiddlewaretoken', None)
            sheet_name = parameters.pop('sheet_name',None)
            data_df = pd.DataFrame(parameters)
            print('data_df',data_df)
            is_valid,errors = mainValidate_function(sheet_name,data_df)
            return JsonResponse({'is_valid': is_valid, 'errors': errors})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



class Threshold_Logic_ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold_Logic_Config
        fields = '__all__'


# @login_required
# class Threshold_Logic_Config_get_data(APIView):
#     def get(self, request, pk):
#         try:
#             instance = Threshold_Logic_Config.objects.get(pk=pk)
        
#         except Threshold_Logic_Config.DoesNotExist:
#             return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        
#         serializer = Threshold_Logic_ConfigSerializer(instance)
#         return Response(serializer.data)
@csrf_exempt
@login_required
@api_view(['GET'])
def threshold_logic_config_detail_view(request, pk):
    try:
        instance = Threshold_Logic_Config.objects.get(pk=pk)
    except Threshold_Logic_Config.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Threshold_Logic_ConfigSerializer(instance)
    print(serializer)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def delete_data_by_id(request, row_id):
    try:
        # Assuming YourModel has a primary key named 'id'
        print(row_id)
        instance = Threshold_Logic_Config.objects.get(trigger_id=row_id)
        instance.delete()
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)


class Trigg_Thres_By_Business_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Trigg_Thres_By_Business
        fields = '__all__'




@csrf_exempt
@login_required
@api_view(['GET'])
def Trigg_Thres_By_Business_view(request, pk):
    try:
        instance = Trigg_Thres_By_Business.objects.get(pk=pk)
    except Trigg_Thres_By_Business.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Trigg_Thres_By_Business_Serializer(instance)
    print(serializer)
    return Response(serializer.data)

# ##################insert the config data into the model###################
# def insert_config_data(df):
#     print(df.columns)
#     for index, row in df.iterrows():
#         threshold_logic_config = Threshold_Logic_Config(
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
#         threshold_logic_config.save()
# df = pd.read_excel('Config Template 081123.xlsx', sheet_name='1.a Threshold Logic Config',skiprows=1)
# insert_config_data(df)

# ##################CRED Operations#######################
# # Create
# threshold = Threshold_Logic_Config(
#     trigger_id=1,
#     trigg_desc="If Last N month's avg TAT between lead generation and set up of meeting...",
#     # ... (other fields)
# )
# threshold.save()
# Read
# queryset = Threshold_Logic_Config.objects.all()
# df = pd.DataFrame(list(queryset.values()))
# print(df.to_string(index=False))
# # Update
# threshold = Threshold_Logic_Config.objects.get(trigger_id=1)
# threshold.trigg_desc = "Updated description"
# threshold.save()
# # Delete
# threshold = Threshold_Logic_Config.objects.get(trigger_id=1)
# threshold.delete()
# ###########################################################

# ##################insert the config data into the model###################
# def insert_config_data_1(df):
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
# insert_config_data_1(df)


# #################insert the config data into the model###################
# def insert_channel_task_mapping_data(df):
#     for index, row in df.iterrows():
#         channel_task_mapping = Channel_Task_Mapping(
#             Channel=row['Channel'],
#             Channel_Subchannel_ID=row['Channel_Subchannel_ID'],
#             channel_subchannel_Name=row['channel_subchannel_Name'],
#             DemoSeg_ValueSeg_ID=row['DemoSeg_ValueSeg_ID'],
#             DemoSeg_ValueSeg_Name=row['DemoSeg_ValueSeg_Name'],
#             Task=row['Task']
#         )
#         channel_task_mapping.save()
# df_channel_task_mapping = pd.read_excel('Config Template 081123.xlsx', sheet_name='3.a Channel_Task_Mapping')
# print(df_channel_task_mapping)
# insert_channel_task_mapping_data(df_channel_task_mapping)



# def insert_task_trigger_mapping_data(df):
#     for index, row in df.iterrows():
#         task_trigger_mapping = Task_Trigger_Mapping(
#             Task_id=row['Task_id'],
#             Task_Desc=row['Task_Desc'],
#             Task_Stage=row['Task_Stage'],
#             Trigger=row['Trigger']
#         )
#         task_trigger_mapping.save()
# df_task_trigger_mapping = pd.read_excel('Config Template 081123.xlsx', sheet_name='3.b Task_Trigger_Mapping', skiprows=1)
# insert_task_trigger_mapping_data(df_task_trigger_mapping)


# def insert_trigger_on_query_logic_data(df):
#     for index, row in df.iterrows():
#         trigger_on_query_logic = Trigger_ON_Query(
#             Trigger_id=row['Trigger_id'],
#             Trigger_Description_Discussed=row['Trigger_Description_Discussed'],
#             Assignment_level=row['Assignment_level'],
#             Iteration_Level=row['Iteration_Level'],
#             Trigger_ON_Query_Logic=row['Trigger_ON_Query_Logic'],
#             query=row['query']
#         )
#         trigger_on_query_logic.save()

# df_trigger_on_query_logic = pd.read_excel('Config Template 081123.xlsx', sheet_name='3.c Trigger_ON_Query', skiprows=1)
# insert_trigger_on_query_logic_data(df_trigger_on_query_logic)




# def insert_optimization_rules_data(df):
#     for index, row in df.iterrows():
#         optimization_rule = Task_Constraint_Rules(
#             Task_No=row['Task No'],
#             Constraint_Description=row['Constraint Description'],
#             Category_Task_Associated_with=row['Category Task Associated with'],
#             Min_Task_Count_FLS=row['Min Task Count/FLS'],
#             Max_Task_Count_FLS=row['Max Task Count/FLS'],
#             Mutual_Exclusion_Criteria=row['Mutual Exclusion Criteria'],
#             Task_Priority=row['Task Priority']
#         )
#         optimization_rule.save()
# df_optimization_rules = pd.read_excel('Config Template 081123.xlsx', sheet_name='4.a Task Constraint Rules', skiprows=3)
# insert_optimization_rules_data(df_optimization_rules)


# def insert_allocation_parameters_data(df):
#     for index, row in df.iterrows():
#         allocation_parameter = Allocation_Parameters(
#             Task_id=row['Task_id'],
#             Channel=row['Channel'],
#             Subchannel=row['Subchannel'],
#             DemoSeg=row['DemoSeg'],
#             ValueSeg=row['ValueSeg'],
#             Segment_id=row['Segment_id'],
#             Due_Days=row['Due_Days'],
#             Buffer_Days=row['Buffer Days'],
#             XX_Value=row['XX_Value'],
#             XX_Type=row['XX_Type'],
#             PricePoint_Reward=row['PricePoint(Reward)']
#         )
#         allocation_parameter.save()


# df_allocation_parameters = pd.read_excel('Config Template 081123.xlsx', sheet_name='4.b Allocation Parameters', skiprows=1)
# insert_allocation_parameters_data(df_allocation_parameters)

# def insert_microseg_default_tasks_data(df):
#     for index, row in df.iterrows():
#         microsegment_Default_Tasks = Microsegment_Default_Tasks(
#             Channel=row['Channel'],
#             Subchannel=row['Subchannel'],
#             DemoSeg=row['DemoSeg'],
#             ValueSeg=row['ValueSeg'],
#             Segment_id=row['Segment_id'],
#             Default_Tasks=row['Default_Tasks']
#         )
#         microsegment_Default_Tasks.save()


# df_allocation_parameters = pd.read_excel('Config Template 081123.xlsx', sheet_name='4.c Microsegment Default Tasks', skiprows=1)
# insert_microseg_default_tasks_data(df_allocation_parameters)


# def insert_fls_avg_threshold_output_data(df):
#     for index, row in df.iterrows():
#         default_Channel_Trigg_thres = Default_Channel_Trigg_thres(
#             Channel=row['Channel'],
#             Trigger_id=row['Trigger_id'],
#             Trigg_Desc =row['Trigg_Desc'],
#             Segment_Threshold_1=row['Segment_Threshold_1']
#             FLSAvg_Threshold_2=row['FLSAvg_Threshold_2']
#         )
#         default_Channel_Trigg_thres.save()

# # Read data from Excel file
# df_fls_avg_threshold_output = pd.read_excel('Config Template 081123.xlsx', sheet_name='1.c Default_Channel_Trigg_thres', skiprows=1)

# # Insert data into the FLS_Avg_Threshold_Output model
# insert_fls_avg_threshold_output_data(df_fls_avg_threshold_output)


# def insert_task_closure_config_data(df):
#     for index, row in df.iterrows():
#         task_closure_config = Task_Closure_Config(
#             Task_id=row['Task_id'],
#             Task_Desc=row['Task_Desc'],
#             Closure_True_Query=row['Closure_True_Query']
#         )
#         task_closure_config.save()

# df_task_closure_config = pd.read_excel('Config Template 081123.xlsx', sheet_name='2.a Task Closure Config', skiprows=1)
# print(df_task_closure_config)
# insert_task_closure_config_data(df_task_closure_config)


def upload_to_s3(request,sheet_name):
    try:
        # sheet_name = request.POST.get('sheet_name')
        data_model = apps.get_model(app_label='app_validation',model_name=sheet_name)
        data_df = pd.DataFrame(list(data_model.objects.all().values()))
        is_valid, errors = mainValidate_function(sheet_name, data_df)
        if not is_valid:
            return JsonResponse({'error': errors}, status = 400)
        is_valid, errors = s3_upload(data_df,sheet_name,s3_bucket,s3_path)
        if not is_valid:
            return JsonResponse({'error': errors}, status = 400)
        return JsonResponse({'message': 'Success'}, status = 200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = 400)
