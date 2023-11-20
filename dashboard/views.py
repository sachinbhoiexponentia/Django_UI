from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_validation.models import *
import pandas as pd



@login_required
def Threshold_Login_Config_view(request):
    
    # Threshold_Logic_Config
    queryset = Threshold_Login_Config.objects.all()
    Threshold_Login_Config_df = pd.DataFrame(list(queryset.values()))
    Threshold_Login_Config_headers = list(Threshold_Login_Config_df.columns)
    Threshold_Login_Config_data = Threshold_Login_Config_df.values.tolist()

    # Threshold_Logic_Config
    queryset1 = Trigg_Thres_By_Business.objects.all()
    Trigg_Thres_By_Business_df = pd.DataFrame(list(queryset1.values()))
    Trigg_Thres_By_Business_headers = list(Trigg_Thres_By_Business_df.columns)
    Trigg_Thres_By_Business_data = Trigg_Thres_By_Business_df.values.tolist()

    
    queryset2 = Segment_Threshold_Output.objects.all()
    Segment_Threshold_Output_df = pd.DataFrame(list(queryset2.values()))
    # print('Segment_Threshold_Output_df',Segment_Threshold_Output_df)
    Segment_Threshold_Output_headers = list(Segment_Threshold_Output_df.columns)
    Segment_Threshold_Output_data = Segment_Threshold_Output_df.values.tolist()

    queryset3 = FLS_Avg_Threshold_Output.objects.all()
    FLS_Avg_Threshold_Output_df = pd.DataFrame(list(queryset3.values()))
    FLS_Avg_Threshold_Output_headers = list(FLS_Avg_Threshold_Output_df.columns)
    FLS_Avg_Threshold_Output_data = FLS_Avg_Threshold_Output_df.values.tolist()

    context = {'FLS_Avg_Threshold_Output_headers':FLS_Avg_Threshold_Output_headers,'FLS_Avg_Threshold_Output_data':FLS_Avg_Threshold_Output_data ,'Segment_Threshold_Output_data':Segment_Threshold_Output_data,
              'Segment_Threshold_Output_headers':Segment_Threshold_Output_headers,'Trigg_Thres_By_Business_headers':Trigg_Thres_By_Business_headers,'Threshold_Login_Config_headers': Threshold_Login_Config_headers, 
            'Threshold_Login_Config_data': Threshold_Login_Config_data,'Trigg_Thres_By_Business_data':Trigg_Thres_By_Business_data}

    if request.method == 'POST':
        print('Django post request')
        form_id = request.POST.get('form_identifier')
        if form_id == 'Threshold_Logic_Form':
            print('Threshold_Logic_Form')
            data = request.POST
            # parameters = dict(data.lists())
            # print('parameters',parameters)
            # if 'csrfmiddlewaretoken' in parameters:
                # csrf_token = parameters.pop('csrfmiddlewaretoken', None)
            # data_df = pd.DataFrame(parameters)
            # print('data_df',data_df)
            threshold_login_config = Threshold_Login_Config(
                trigger_id=request.POST.get('Trigger_id'),
                trigg_desc=request.POST.get('Trigg_Desc'),
                thres_description=request.POST.get('Thres_Description'),
                thres_query_logic=request.POST.get('Thres_Query_Logic'),
                operation=request.POST.get('Operation'),
                analysis_period=request.POST.get('Analysis_Period'),
                num_thresholds_required=request.POST.get('Num_Threshold_Required'),
                segment_threshold_requirement_flag=request.POST.get('Segment_Threshold_Requirement_Flag'),
                FLS_Threshold_Requirement_Flag=request.POST.get('FLS_Threshold_Requirement_Flag'))
            threshold_login_config.save()
        
    return render(request, 'Threshold_logic.html', context)


@login_required
def closure_Config_view(request):
    queryset = Task_Closure_Config.objects.all()
    Task_Closure_Config_df = pd.DataFrame(list(queryset.values()))
    Task_Closure_Config_headers = list(Task_Closure_Config_df.columns)
    Task_Closure_Config_data = Task_Closure_Config_df.values.tolist()

    context = {'Task_Closure_Config_headers':Task_Closure_Config_headers,'Task_Closure_Config_data':Task_Closure_Config_data }
    return render(request,'closure_logic.html',context)



@login_required
def TNT_Module_View(request):
    # Fetch data for Channel_Task_Mapping
    queryset_channel_task_mapping = Channel_Task_Mapping.objects.all()
    channel_task_mapping_df = pd.DataFrame(list(queryset_channel_task_mapping.values()))
    channel_task_mapping_headers = list(channel_task_mapping_df.columns)
    channel_task_mapping_data = channel_task_mapping_df.values.tolist()

    # Fetch data for Task_Trigger_Mapping
    queryset_task_trigger_mapping = Task_Trigger_Mapping.objects.all()
    task_trigger_mapping_df = pd.DataFrame(list(queryset_task_trigger_mapping.values()))
    task_trigger_mapping_headers = list(task_trigger_mapping_df.columns)
    task_trigger_mapping_data = task_trigger_mapping_df.values.tolist()

    # Fetch data for Trigger_ON_Query_Logic
    queryset_trigger_query_logic = Trigger_ON_Query_Logic.objects.all()
    trigger_query_logic_df = pd.DataFrame(list(queryset_trigger_query_logic.values()))
    trigger_query_logic_headers = list(trigger_query_logic_df.columns)
    trigger_query_logic_data = trigger_query_logic_df.values.tolist()

    context = {
        'channel_task_mapping_data_headers': channel_task_mapping_headers,
        'channel_task_mapping_data_data': channel_task_mapping_data,
        'task_trigger_mapping_data_headers': task_trigger_mapping_headers,
        'task_trigger_mapping_data_data': task_trigger_mapping_data,
        'trigger_query_logic_data_headers': trigger_query_logic_headers,
        'trigger_query_logic_data_data': trigger_query_logic_data}
    
    return render(request, 'TNT.html',context)


def TOAM_Module_View(request):
    # Fetch data for Optimization_Rules
    queryset_optimization_rules = Optimization_Rules.objects.all()
    optimization_rules_df = pd.DataFrame(list(queryset_optimization_rules.values()))
    optimization_rules_headers = list(optimization_rules_df.columns)
    optimization_rules_data = optimization_rules_df.values.tolist()

    # Fetch data for Allocation_Parameters
    queryset_allocation_parameters = Allocation_Parameters.objects.all()
    allocation_parameters_df = pd.DataFrame(list(queryset_allocation_parameters.values()))
    allocation_parameters_headers = list(allocation_parameters_df.columns)
    allocation_parameters_data = allocation_parameters_df.values.tolist()

    # Fetch data for Product_Mix_Focus
    queryset_product_mix_focus = Product_Mix_Focus.objects.all()
    product_mix_focus_df = pd.DataFrame(list(queryset_product_mix_focus.values()))
    product_mix_focus_headers = list(product_mix_focus_df.columns)
    product_mix_focus_data = product_mix_focus_df.values.tolist()

    context = {
        'optimization_rules_data_headers': optimization_rules_headers,
        'optimization_rules_data_data': optimization_rules_data,
        'allocation_parameters_data_headers': allocation_parameters_headers,
        'allocation_parameters_data_data': allocation_parameters_data,
        'product_mix_focus_data_headers': product_mix_focus_headers,
        'product_mix_focus_data_data': product_mix_focus_data,}
    
    return render(request, 'TOAM.html',context)