from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from app_validation.models import *
from .controller import *
import pandas as pd

@csrf_exempt
@login_required 
def validate_thresold_config_df_api(request):
    print("validate_thresold_config_df_api function")
    if request.method == 'GET':
        print('GET Method')
        try:
            data = request.GET
            print('data',data)
            parameters = dict(data.lists())
            print('parameters',parameters)
            if 'csrfmiddlewaretoken' in parameters:
                csrf_token = parameters.pop('csrfmiddlewaretoken', None)
            data_df = pd.DataFrame(parameters)

            is_valid,errors = False, ['data_df']
            return JsonResponse({'is_valid': is_valid, 'errors': errors})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)







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


##################insert the config data into the model###################
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
#         trigger_on_query_logic = Trigger_ON_Query_Logic(
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
#         optimization_rule = Optimization_Rules(
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

# queryset = Allocation_Parameters.objects.all()
# df = pd.DataFrame(list(queryset.values()))
# print(df)






# def insert_product_mix_focus_data(df):
#     for index, row in df.iterrows():
#         product_mix_focus = Product_Mix_Focus(
#             Channel=row['Channel'],
#             Subchannel=row['Subchannel'],
#             DemoSeg=row['DemoSeg'],
#             ValueSeg=row['ValueSeg'],
#             Focus_Product=row['Focus Product'],
#             prod_mix_non_par_annuity_immediate=row['prod_mix_non_par_annuity_immediate'],
#             prod_mix_non_par_c2p=row['prod_mix_non_par_c2p'],
#             prod_mix_non_par_sanchay=row['prod_mix_non_par_sanchay'],
#             prod_mix_non_par_annuity_pgp=row['prod_mix_non_par_annuity_pgp'],
#             prod_mix_non_par_health=row['prod_mix_non_par_health'],
#             prod_mix_par_others=row['prod_mix_par_others'],
#             prod_mix_par_ppt_10=row['prod_mix_par_ppt_10+'],
#             prod_mix_ul_others=row['prod_mix_ul_others'],
#             prod_mix_ul_ppt_10=row['prod_mix_ul_ppt_10+'],
#             prod_mix_ul_single_pre=row['prod_mix_ul_single_pre']
#         )
#         product_mix_focus.save()
        
# df_product_mix_focus = pd.read_excel('Config Template 081123.xlsx', sheet_name='4.d Product Mix Focus', skiprows=1)
# print(df_product_mix_focus)


# queryset = Product_Mix_Focus.objects.all()
# df = pd.DataFrame(list(queryset.values()))
# print(df)




# def insert_segment_threshold_output_data(df):
#     for index, row in df.iterrows():
#         segment_threshold_output = Segment_Threshold_Output(
#             Channel=row['Channel'],
#             Subchannel=row['Subchannel'],
#             Channel_Subchannel_ID=row['Channel_Sunchannel_ID'],
#             DemoSeg=row['DemoSeg'],
#             ValueSeg=row['ValueSeg'],
#             DemoSeg_ValueSeg_ID=row['DemoSeg_ValueSeg_ID'],
#             Trigger_id=row['Trigger_id'],
#             Segment_Threshold=row['Segment_Threshold']
#         )
#         segment_threshold_output.save()

# df_segment_threshold_output = pd.read_excel('Config Template 081123.xlsx', sheet_name='1.c Segment_thres1_output', skiprows=1)

# insert_segment_threshold_output_data(df_segment_threshold_output)


# def insert_fls_avg_threshold_output_data(df):
#     for index, row in df.iterrows():
#         fls_avg_threshold_output = FLS_Avg_Threshold_Output(
#             FLS_id=row['FLS_id'],
#             Channel=row['Channel'],
#             Subchannel=row['Subchannel'],
#             Channel_Subchannel_ID=row['Channel_Sunchannel_ID'],
#             DemoSeg=row['DemoSeg'],
#             ValueSeg=row['ValueSeg'],
#             DemoSeg_ValueSeg_ID=row['DemoSeg_ValueSeg_ID'],
#             Trigger_id=row['Trigger_id'],
#             FLSAvg_Threshold=row['FLSAvg_Threshold']
#         )
#         fls_avg_threshold_output.save()

# # Read data from Excel file
# df_fls_avg_threshold_output = pd.read_excel('Config Template 081123.xlsx', sheet_name='1.d FLS_Avg_thres2_output', skiprows=1)

# # Insert data into the FLS_Avg_Threshold_Output model
# insert_fls_avg_threshold_output_data(df_fls_avg_threshold_output)