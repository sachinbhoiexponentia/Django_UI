import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from app_validation.models import *
from django.apps import apps
from .controller import *
from .config import s3_bucket,s3_path
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import csv
import dashboard 

# parameters {'csrfmiddlewaretoken': ['02cZJmkYFysNRmS77fTJ20TPQXof0wShpP6VAlU35vxY3WruxjGNtYLiWw9YvfPW', '02cZJmkYFysNRmS77fTJ20TPQXof0wShpP6VAlU35vxY3WruxjGNtYLiWw9YvfPW'], 'form_identifier': ['Trigger_Threhold_by_Business_Form'], 'channel': [''], 'subchannel': [''], 'channel_subchannel_id': [''], 'demoseg': [''], 'valueseg': [''], 'demoseg_valueseg_id': [''], 'trigger_id': [''], 'trigg_description': [''], 'segment_threshold_1': [''], 'flavg_threshold': ['']}
#done
@csrf_exempt
@login_required 
def validate_thresold_config_df_api(request):
    # return JsonResponse({'is_valid': True, 'errors': []})
    print("validate_thresold_config_df_api function")
    if request.method == 'GET':
        is_valid = False
        errors = []
        print('GET Method')
        # try:
            # return JsonResponse({'is_valid': True, 'errors': ['errors']})
        data = request.GET
        parameters = dict(data.lists())
        print('parameters',parameters)
        sheet_name = data.get('form_identifier')
        # sheet_name = config_sheets[sheet_name]
        print('sheet_name',sheet_name)
        
        if 'csrfmiddlewaretoken' in parameters:
            csrf_token = parameters.pop('csrfmiddlewaretoken', None)
        data_df = pd.DataFrame(parameters)
        if 'form_identifier' in data_df.columns:
            data_df = data_df.drop('form_identifier', axis=1)
            
        # if sheet_name == 'Threshold_Logic_Form':
        #     is_valid,errors = validate_thresold_config_df(data_df)
        # if sheet_name == 'Trigger_Threhold_by_Business_Form':
        #     is_valid,errors = validate_Trigg_thres_bussness(data_df)
        # if sheet_name == 'closure_form':
        #     is_valid,errors = validate_Task_Closure_Config(data_df)
        # if sheet_name == 'channel_task_mapping_Form':
        #     is_valid,errors = validate_Channel_Task_Mapping(data_df)
        # if sheet_name == 'task_trigger_mapping_Form':
        #     is_valid,errors = Validate_Task_Trigger_Mapping(data_df)
        # if sheet_name == 'trigger_on_query_logic_Form':
        #     is_valid,errors = validate_Trigger_ON_Query(data_df)
        # if sheet_name == 'optimization_rules_Form':
        #     is_valid,errors = validate_task_constraint_rules(data_df) 
        # if sheet_name == 'allocation_parameters_Form':
        #     is_valid,errors = validate_allocation_parameters(data_df) 
        # if sheet_name == 'microsegment_default_tasks_Form':
        #     is_valid,errors = validate_microseg_default_tasks(data_df) 
        # try:
        is_valid,errors = mainValidate_function(sheet_name,data_df)
        print('is_valid,errors',is_valid,errors)
        # except:
            # is_valid = False
            # errors = ['Validation module failes']
        return JsonResponse({'is_valid': is_valid, 'errors': errors})
        # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




############################# Threshold_Login_Config edit and delete ##########################
class Threshold_Logic_ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold_Logic_Config
        fields = '__all__'

@csrf_exempt
@login_required
@api_view(['GET'])
def threshold_logic_config_detail_view(request, pk):
    print('threshold_logic_config_detail_view pk',pk)
    try:
        instance = Threshold_Logic_Config.objects.get(pk=pk)
        print("instance:",instance)
    except Threshold_Logic_Config.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Threshold_Logic_ConfigSerializer(instance)
    print(serializer.data)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def threshold_logic_config_delete_data_by_id(request, row_id):
    try:
        # Assuming YourModel has a primary key named 'id'
        print(row_id)
        instance = Threshold_Logic_Config.objects.get(trigger_id=row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Threshold_Logic_Config')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
###############################################################################################
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


@csrf_exempt
@login_required
@require_POST
def Trigg_Thres_By_Business_delete_data_by_id(request, row_id):
    try:
        print(row_id)
        instance = Trigg_Thres_By_Business.objects.get(id=row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Trigg_Thres_By_Business')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)

############################# Channel_Task_Mapping edit and delete ##########################
class Channel_Task_MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel_Task_Mapping
        fields = '__all__'

@csrf_exempt
@login_required
@api_view(['GET'])
def channel_task_mapping_detail_view(request, pk):
    print('pk',pk)
    try:
        instance = Channel_Task_Mapping.objects.get(id=pk)
        print('instance',instance)
    except Channel_Task_Mapping.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Channel_Task_MappingSerializer(instance)
    print('serializer',serializer.data)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def channel_task_mapping_delete_data_by_id(request, row_id):
    try:
        print(row_id)
        instance = Channel_Task_Mapping.objects.get(id=row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Channel_Task_Mapping')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
###############################################################################################
class Default_Channel_Trigg_thres_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Default_Channel_Trigg_thres
        fields = '__all__'


@csrf_exempt
@login_required
@api_view(['GET'])
def Default_Channel_Trigg_thres_view(request, pk):
    try:
        print("pk:",pk)
        instance = Default_Channel_Trigg_thres.objects.get(pk=pk)
        print("instance:",instance)
    except Default_Channel_Trigg_thres.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Default_Channel_Trigg_thres_Serializer(instance)
    print(serializer)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def Default_Channel_Trigg_thres_delete_data_by_id(request, row_id):
    try:
        print(row_id)
        instance = Default_Channel_Trigg_thres.objects.get(id=row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Default_Channel_Trigg_thres')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)

############################# Trigger_ON_Query edit and delete ##########################
class Trigger_ON_QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger_ON_Query
        fields = '__all__'
        
@csrf_exempt
@login_required
@api_view(['GET'])
def trigger_on_query_detail_view(request, Trigger_id):
    try:
        instance = Trigger_ON_Query.objects.get(Trigger_id=Trigger_id)
    except Trigger_ON_Query.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = Trigger_ON_QuerySerializer(instance)
    print('serializer data',serializer.data)
    return Response(serializer.data)


@csrf_exempt
@login_required
@require_POST
def trigger_on_query_delete_data_by_id(request, Trigger_id):
    try:
        instance = Trigger_ON_Query.objects.get(Trigger_id=Trigger_id)
        instance.delete()
        dashboard.views.upload_to_s3('Trigger_ON_Query')
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
###############################################################################################




############################# TaskTriggerMapping edit and delete ##########################
class TaskTriggerMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Trigger_Mapping
        fields = '__all__'
        
@csrf_exempt
@login_required
@api_view(['GET'])
def task_trigger_mapping_detail_view(request, task_id):
    try:
        instance = Task_Trigger_Mapping.objects.get(Task_id=task_id)
    except Task_Trigger_Mapping.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskTriggerMappingSerializer(instance)
    print('serializer data',serializer.data)
    return Response(serializer.data)


@csrf_exempt
@login_required
@require_POST
def task_trigger_mapping_delete_data_by_id(request, task_id):
    try:
        instance = Task_Trigger_Mapping.objects.get(Task_id=task_id)
        instance.delete()
        dashboard.views.upload_to_s3('Task_Trigger_Mapping')
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
###############################################################################################



############################# closure edit and delete ##########################
class Task_Closure_ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Closure_Config
        fields = '__all__'

@csrf_exempt
@login_required
@api_view(['GET'])
def task_closure_detail_view(request, pk):
    try:
        instance = Task_Closure_Config.objects.get(pk=pk)
    except Task_Closure_Config.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Task_Closure_ConfigSerializer(instance)
    print(serializer)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def task_closure_delete_by_id(request, row_id):
    try:
        print(row_id)
        instance = Task_Closure_Config.objects.get(pk=row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Task_Closure_Config')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
###############################################################################################





############################# Allocation_Parameters_DataSerializer edit and delete ##########################
class Allocation_Parameters_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation_Parameters
        fields = '__all__'


@csrf_exempt
@login_required
@api_view(['GET'])
def allocation_parameters_detail_view(request, pk):
    print('pk',pk)
    try:
        instance = Allocation_Parameters.objects.get(pk=pk)
    except Allocation_Parameters.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Allocation_Parameters_DataSerializer(instance)
    print(serializer.data)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def allocation_parameters_delete_by_id(request, row_id):
    try:
        # Assuming YourModel has a primary key named 'id'
        print(row_id)
        instance = Allocation_Parameters.objects.get(pk = row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Allocation_Parameters')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
##############################################################################################










############################# Microsegment_Default_Tasks edit and delete ##########################
class Microsegment_Default_TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microsegment_Default_Tasks
        fields = '__all__'
        
@csrf_exempt
@login_required
@api_view(['GET'])
def microsegment_default_tasks_detail_view(request, mdt_pk_id):
    try:
        instance = Microsegment_Default_Tasks.objects.get(id=mdt_pk_id)
    except Microsegment_Default_Tasks.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = Microsegment_Default_TasksSerializer(instance)
    print('serializer data',serializer.data)
    return Response(serializer.data)


@csrf_exempt
@login_required
@require_POST
def microsegment_default_tasks_delete_data_by_id(request, mdt_pk_id):
    try:
        instance = Microsegment_Default_Tasks.objects.get(id=mdt_pk_id)
        instance.delete()
        dashboard.views.upload_to_s3('Microsegment_Default_Tasks')
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
###############################################################################################



class Product_Category_Config_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category_Config
        fields = '__all__'


@csrf_exempt
@login_required
@api_view(['GET'])
def Product_Category_Config_view(request, pk):
    try:
        print("pk:",pk)
        instance = Product_Category_Config.objects.get(pk=pk)
        print("instance:",instance)
    except Product_Category_Config.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Product_Category_Config_Serializer(instance)
    print(serializer)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def Product_Category_Config_delete_data_by_id(request, row_id):
    try:
        print(row_id)
        instance = Product_Category_Config.objects.get(id=row_id)
        instance.delete()
        dashboard.views.upload_to_s3('Product_Category_Config')
        print("Deleted Successfuly")
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)





# @login_required
# class Threshold_Login_Config_get_data(APIView):
#     def get(self, request, pk):
#         try:
#             instance = Threshold_Login_Config.objects.get(pk=pk)
        
#         except Threshold_Login_Config.DoesNotExist:
#             return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        
#         serializer = Threshold_Login_ConfigSerializer(instance)
#         return Response(serializer.data)

class Task_Constraint_Rules_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Constraint_Rules
        fields = '__all__'


@csrf_exempt
@login_required
@api_view(['GET'])
def task_constraint_rules_detail_view(request, pk):
    print('pk',pk)
    try:
        instance = Task_Constraint_Rules.objects.get(pk=pk)
    except Task_Constraint_Rules.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Task_Constraint_Rules_DataSerializer(instance)
    print(serializer)
    return Response(serializer.data)

@csrf_exempt
@login_required
@require_POST
def task_constraint_rules_delete_by_id(request, row_id):
    try:
        # Assuming YourModel has a primary key named 'id'
        print(row_id)
        instance = Task_Constraint_Rules.objects.get(Task_No = row_id)
        instance.delete()
        print("Deleted Successfuly")
        dashboard.views.upload_to_s3('Task_Constraint_Rules')
        return JsonResponse({'message': 'Data deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Object not found'}, status=404)
    

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
#             Closure_True_Query=row['Closure_True_Query'],
#             Closure_SQL_Query=row['Closure_SQL_Query']
#         )
#         task_closure_config.save()

# df_task_closure_config = pd.read_excel('Config Template 081123.xlsx', sheet_name='2.a Task Closure Config', skiprows=1)
# print(df_task_closure_config)
# insert_task_closure_config_data(df_task_closure_config)

# Task_Closure_Config.objects.all().delete()



# #################insert the config data into the model###################
# def insert_channel_task_mapping_data(df):
#     for index, row in df.iterrows():
#         default_Channel_Trigg_thres= Default_Channel_Trigg_thres(
#             Channel=row['Channel'],
#             Trigger_id=row['Trigger_id'],
#             Trigg_Desc=row['Trigg_Desc'],
#             Segment_Threshold_1=row['Segment_Threshold_1'],
#             FLSAvg_Threshold_2=row['FLSAvg_Threshold_2']
#         )
#         default_Channel_Trigg_thres.save()
# default_Channel_Trigg_thres = pd.read_excel('Config Template 081123.xlsx', sheet_name='3.a Channel_Task_Mapping')
# print(default_Channel_Trigg_thres)
# insert_channel_task_mapping_data(default_Channel_Trigg_thres)


# dummy_record = Microsegment_Default_Tasks.objects.create(
#     Channel='Default Channel',
#     Subchannel='Default Subchannel',
#     DemoSeg=1.0, 
#     ValueSeg=1.0, 
#     Segment_id=1.0,  
#     Default_Tasks='Default Task List')
# dummy_record.save()
# print('dummy records saved')


# def upload_to_s3(request,sheet_name):
#     try:
#         # sheet_name = request.POST.get('sheet_name')
#         data_model = apps.get_model(app_label='app_validation',model_name=sheet_name)
#         data_df = pd.DataFrame(list(data_model.objects.all().values()))
#         is_valid, errors = mainValidate_function(sheet_name, data_df)
#         if not is_valid:
#             return JsonResponse({'error': errors}, status = 400)
#         is_valid, errors = s3_upload(data_df,sheet_name,s3_bucket,s3_path)
#         if not is_valid:
#             return JsonResponse({'error': errors}, status = 400)
#         return JsonResponse({'message': 'Success'}, status = 200)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status = 400)



# # Inserting dummy rows
# dummy_rows = [
#     {
#         "ProductCategoryName": "Category1",
#         "FilterQueryOnPolicyTable": "FilterQuery1",
#         "TrainingTopics": "Topic1",
#         "SellingTaskNo": "TaskNo1",
#         "TrainingTaskNo": "TrainingTaskNo1",
#     },
#     {
#         "ProductCategoryName": "Category2",
#         "FilterQueryOnPolicyTable": "FilterQuery2",
#         "TrainingTopics": "Topic2",
#         "SellingTaskNo": "TaskNo2",
#         "TrainingTaskNo": "TrainingTaskNo2",
#     },
#     # Add more dummy rows as needed
# ]

# for dummy_row in dummy_rows:
#     Product_Category_Config.objects.create(**dummy_row)

# print("Dummy rows inserted successfully.")
    
@csrf_exempt
@login_required
@api_view(['GET'])
def upload_to_s3(request, sheet_name):   # maybe not in use, delete it
    try:
        print("upload to s3")
        # sheet_name = request.POST.get('sheet_name')
        data_model = apps.get_model(app_label='app_validation', model_name=sheet_name)
        data_df = pd.DataFrame(list(data_model.objects.all().values()))
        print("upload data_df:",data_df)
        # is_valid, errors = mainValidate_function(sheet_name, data_df)
        # Save to a local CSV file
        local_file_path = f"upload_csv_files/{sheet_name}_local_data.csv"
        data_df.to_csv(local_file_path, index=False)

        # Optionally, you can return the local file path in the response
        return JsonResponse({'is_valid': True, 'errors': ['errors']})
    except Exception as e:
        return JsonResponse({'is_valid': False, 'errors': [e]})


@csrf_exempt
@login_required
def csv_download(request):
    data = request.GET
    sheet_name = data.get('form_identifier')
    print(sheet_name)
    if sheet_name == 'Product_Category_Form':
        queryset = Product_Category_Config.objects.all()
    if sheet_name == 'Threshold_Logic_Form':
        queryset = Threshold_Logic_Config.objects.all()
    if sheet_name == 'Trigger_Threhold_by_Business_Form':
        queryset = Trigg_Thres_By_Business.objects.all()
    if sheet_name == 'closure_form':
        queryset = Task_Closure_Config.objects.all()
    if sheet_name == 'channel_task_mapping_Form':
        queryset = Channel_Task_Mapping.objects.all()
    if sheet_name == 'task_trigger_mapping_Form':
        queryset = Task_Trigger_Mapping.objects.all()
    if sheet_name == 'trigger_on_query_logic_Form':
        queryset = Trigger_ON_Query.objects.all()
    if sheet_name == 'optimization_rules_Form':
        queryset = Task_Constraint_Rules.objects.all()
    if sheet_name == 'allocation_parameters_Form':
        queryset = Allocation_Parameters.objects.all()
    if sheet_name == 'microsegment_default_tasks_Form':
        queryset = Microsegment_Default_Tasks.objects.all()
    results = pd.DataFrame(list(queryset.values()))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{sheet_name}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(results.columns)
    for row in results.index:
        # print(results.loc(row).tolist())
        writer.writerow(results.loc[row].tolist())
    # results.to_csv(path_or_buf=response)
    print(response)
    return response
