from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_validation.models import *
import pandas as pd
from django.contrib import messages




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
        
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)
        if form_id == 'Threshold_Logic_Form':
            print('Threshold_Logic_Form')
            try:
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
                messages.success(request, 'Form saved successfully')
                return render(request, 'Threshold_logic.html', context)
            except Exception as e:
                print('Error while saving the data ',e)
                messages.error(request, e) 
                
            
        if form_id == 'Trigger_Threhold_by_Business_Form':
            print('Trigger_Threhold_by_Business_Form')
            try:
                trigg_thres_by_business = Trigg_Thres_By_Business(
                    Channel=request.POST.get('channel'),
                    Subchannel=request.POST.get('subchannel'),
                    Channel_Subchannel_ID=request.POST.get('channel_subchannel_id'),
                    DemoSeg=request.POST.get('demoseg'),
                    ValueSeg=request.POST.get('valueseg'),
                    DemoSeg_ValueSeg_ID=request.POST.get('demoseg_valueseg_id'),
                    Trigger_id=request.POST.get('trigger_id'),
                    Trigg_Desc=request.POST.get('trigg_description'),
                    Segment_Threshold=request.POST.get('segment_threshold_1'),
                    FLSAvg_Threshold=request.POST.get('flsavg_threshold')) 
                trigg_thres_by_business.save()
                messages.success(request, 'Form saved successfully')  
                return render(request, 'Threshold_logic.html', context)
            except Exception as e:
                print('Error while saving the data ',e)
                messages.error(request, e) 
        
        if form_id == 'segment_threshold_Form':
            print('segment_threshold_Form')
            try:
                segment_threshold_output = Segment_Threshold_Output(
                Channel=request.POST.get('channel'),
                Subchannel=request.POST.get('subchannel'),
                Channel_Subchannel_ID=request.POST.get('channel_subchannel_id'),
                DemoSeg=request.POST.get('demoseg'),
                ValueSeg=request.POST.get('valueseg'),
                DemoSeg_ValueSeg_ID=request.POST.get('demoseg_valueseg_id'),
                Trigger_id=request.POST.get('trigger_id'),
                Segment_Threshold=request.POST.get('segment_threshold'))
                segment_threshold_output.save()
                messages.success(request, 'Form saved successfully')
                render(request, 'Threshold_logic.html', context)
                return render(request, 'Threshold_logic.html', context)
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)      
                
        if form_id == 'fls_avgthres_Form':
            print('fls_avgthres_Form')
            try:    
                fls_avg_threshold_output = FLS_Avg_Threshold_Output(
                    FLS_id = request.POST.get('fls_id') , 
                    Channel = request.POST.get('channel'),
                    Subchannel = request.POST.get('subchannel'),
                    Channel_Subchannel_ID = request.POST.get('channel_subchannel_id'),
                    DemoSeg = request.POST.get('demoseg'),
                    ValueSeg = request.POST.get('valueseg'),
                    DemoSeg_ValueSeg_ID = request.POST.get('demoseg_valueseg_id'),
                    Trigger_id = request.POST.get('trigger_id'),
                    FLSAvg_Threshold = request.POST.get('flsavg_threshold_2'))
                fls_avg_threshold_output.save()
                messages.success(request, 'Form saved successfully')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)

        if form_id == 'Threshold_Logic_Form_edit':
            print('Threshold_Logic_Form_edit')
            try:
                trigger_id = request.POST.get('Trigger_id_Threshold_Logic_Form_edit')
                print("trigger_id:",trigger_id)
                threshold_login_config = Threshold_Login_Config.objects.get(trigger_id=trigger_id)

                # Update fields based on the form data
                threshold_login_config.trigg_desc = request.POST.get('Trigg_Desc_Threshold_Logic_Form_edit')
                threshold_login_config.thres_description = request.POST.get('Thres_Description_Threshold_Logic_Form_edit')
                threshold_login_config.thres_query_logic = request.POST.get('Thres_Query_Logic_Threshold_Logic_Form_edit')
                threshold_login_config.operation = request.POST.get('Operation_Threshold_Logic_Form_edit')
                threshold_login_config.analysis_period = request.POST.get('Analysis_Period_Threshold_Logic_Form_edit')
                threshold_login_config.num_thresholds_required = request.POST.get('Num_Threshold_Required_Threshold_Logic_Form_edit')
                threshold_login_config.segment_threshold_requirement_flag = request.POST.get('Segment_Threshold_1_Requirement_Flag_Threshold_Logic_Form_edit')
                threshold_login_config.FLS_Threshold_Requirement_Flag = request.POST.get('FLS_Threshold_2_Requirement_Flag_Threshold_Logic_Form_edit')

                threshold_login_config.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'Threshold_logic.html', context)
            except Threshold_Login_Config.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
        
        

    return render(request, 'Threshold_logic.html', context)

 

@login_required
def closure_Config_view(request):
    queryset = Task_Closure_Config.objects.all()
    Task_Closure_Config_df = pd.DataFrame(list(queryset.values()))
    Task_Closure_Config_headers = list(Task_Closure_Config_df.columns)
    Task_Closure_Config_data = Task_Closure_Config_df.values.tolist()

    context = {'Task_Closure_Config_headers':Task_Closure_Config_headers,'Task_Closure_Config_data':Task_Closure_Config_data }

    if request.method == 'POST':
        print('Django post request')
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)    
        if form_id == 'closure_form':
            print('closure_form')
            try:  
                task_closure_config = Task_Closure_Config(
                Task_id = request.POST.get('task_id') , 
                Task_Desc = request.POST.get('task_desc') , 
                Closure_True_Query = request.POST.get('closure_true_query')) 
                task_closure_config.save()
                messages.success(request, 'Form saved successfully')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)

    
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
    
    if request.method == 'POST':
        print('Django post request')
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)    
        if form_id == 'channel_task_mapping_Form':
            print('channel_task_mapping_Form')
            try:
                channel_task_mapping = Channel_Task_Mapping(
                    Channel = request.POST.get('channel') , 
                    Channel_Subchannel_ID = request.POST.get('channel_subchannel_id') , 
                    channel_subchannel_Name = request.POST.get('channel_subchannel_name') , 
                    DemoSeg_ValueSeg_ID = request.POST.get('demoseg_valueseg_id') , 
                    DemoSeg_ValueSeg_Name = request.POST.get('demoseg_valueseg_name') , 
                    Task = request.POST.get('task'))
                channel_task_mapping.save()
                messages.success(request, 'Form saved successfully')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)


        if form_id == 'task_trigger_mapping_Form':
            print('task_trigger_mapping_Form')
            try:
                task_trigger_mapping = Task_Trigger_Mapping(
                Task_id = request.POST.get('task_id') , 
                Task_Desc = request.POST.get('task_desc') , 
                Task_Stage = request.POST.get('task_stage') , 
                Trigger = request.POST.get('trigger'))
                task_trigger_mapping.save()
                messages.success(request, 'Form saved successfully')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)


        if form_id == 'trigger_on_query_logic_Form':
            print('trigger_on_query_logic_Form')
            try:
                trigger_on_query_logic = Trigger_ON_Query_Logic(
                    Trigger_id = request.POST.get('trigger_id') ,
                    Trigger_Description_Discussed = request.POST.get('trigger_description_discussed'),
                    Assignment_level = request.POST.get('assignment_level'),
                    Iteration_Level = request.POST.get('iteration_level'),
                    Trigger_ON_Query_Logic = request.POST.get('trigger_on_query_logic'),
                    query = request.POST.get('query'))
                trigger_on_query_logic.save()
                messages.success(request, 'Form saved successfully')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
            
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
    
    if request.method == 'POST':
        print('Django post request')
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)
        if form_id == 'optimization_rules_Form':
            print('optimization_rules_Form') 
        try:  
            optimization_rules = Optimization_Rules(
                Task_No = request.POST.get('task_no') ,
                Constraint_Description = request.POST.get('constraint') ,
                Category_Task_Associated_with =request.POST.get('category_task_allocated_with') ,
                Min_Task_Count_FLS = request.POST.get('min_task_count_fls') ,
                Max_Task_Count_FLS = request.POST.get('max_task_count_fls') ,
                Mutual_Exclusion_Criteria = request.POST.get('mutual_exclusion_criteria') ,
                Task_Priority =request.POST.get('task_priority') )
            optimization_rules.save()
            messages.success(request, 'Form saved successfully')
        except Exception as e:
            print('Error while saving the data ',e)  
            messages.error(request, e)    
    
    return render(request, 'TOAM.html',context)