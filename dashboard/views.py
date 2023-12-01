from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_validation.models import *
import pandas as pd
from django.contrib import messages



def Threshold_form_success(requests):
    return render(requests, 'threshold_success_page.html')
def Closure_form_success(requests):
    return render(requests, 'closure_success_page.html')
def TNT_form_success(requests):
    return render(requests, 'tnt_success_page.html')
def TOAM_form_success(requests):
    return render(requests, 'toam_success_page.html')


@login_required
def Threshold_Logic_Config_view(request):
    
    # Threshold_Logic_Config
    queryset = Threshold_Logic_Config.objects.all()
    Threshold_Logic_Config_df = pd.DataFrame(list(queryset.values()))
    print(Threshold_Logic_Config_df)
    Threshold_Logic_Config_headers = list(Threshold_Logic_Config_df.columns)
    Threshold_Logic_Config_data = Threshold_Logic_Config_df.values.tolist()

    # Threshold_Logic_Config
    queryset1 = Trigg_Thres_By_Business.objects.all()
    Trigg_Thres_By_Business_df = pd.DataFrame(list(queryset1.values()))
    Trigg_Thres_By_Business_headers = list(Trigg_Thres_By_Business_df.columns)
    Trigg_Thres_By_Business_data = Trigg_Thres_By_Business_df.values.tolist()


    queryset3 = Default_Channel_Trigg_thres.objects.all()
    Default_Channel_Trigg_thres_df = pd.DataFrame(list(queryset3.values()))
    print(Default_Channel_Trigg_thres_df)
    Default_Channel_Trigg_thres_headers = list(Default_Channel_Trigg_thres_df.columns)
    Default_Channel_Trigg_thres_data = Default_Channel_Trigg_thres_df.values.tolist()
    print("Default_Channel_Trigg_thres_headers:",Default_Channel_Trigg_thres_headers)
    print("Default_Channel_Trigg_thres_data:",Default_Channel_Trigg_thres_data)

    context = {'Default_Channel_Trigg_thres_headers':Default_Channel_Trigg_thres_headers,
               'Default_Channel_Trigg_thres_data':Default_Channel_Trigg_thres_data,
               'Trigg_Thres_By_Business_headers':Trigg_Thres_By_Business_headers,
               'Threshold_Logic_Config_headers': Threshold_Logic_Config_headers,
               'Threshold_Logic_Config_data': Threshold_Logic_Config_data,
               'Trigg_Thres_By_Business_data':Trigg_Thres_By_Business_data}

    if request.method == 'POST':
        print('Django post request')
        
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)
        if form_id == 'Threshold_Logic_Form':
            print('Threshold_Logic_Form')
            try:
                threshold_logic_config = Threshold_Logic_Config(
                    trigger_id=request.POST.get('Trigger_id'),
                    trigg_desc=request.POST.get('Trigg_Desc'),
                    thres_description=request.POST.get('Thres_Description'),
                    thres_query_logic=request.POST.get('Thres_Query_Logic'),
                    operation=request.POST.get('Operation'),
                    analysis_period=request.POST.get('Analysis_Period'),
                    num_thresholds_required=request.POST.get('Num_Threshold_Required'),
                    segment_threshold_requirement_flag=request.POST.get('Segment_Threshold_Requirement_Flag'),
                    FLS_Threshold_Requirement_Flag=request.POST.get('FLS_Threshold_Requirement_Flag'))
                threshold_logic_config.save()
                messages.success(request, 'Form saved successfully!')
                return render(request, 'threshold_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)
                messages.error(request, e) 
                return render(request, 'threshold_success_page.html')
                
            
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
                return render(request, 'threshold_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)
                messages.error(request, e) 
                return render(request, 'threshold_success_page.html')
        
                
        if form_id == 'default_channel_trigg_thres_Form':
            print('default_channel_trigg_thres_Form')
            try:    
                default_channel_trigg_thres_output = Default_Channel_Trigg_thres(
                    Channel = request.POST.get('channel'),
                    Trigger_id = request.POST.get('trigger_id'),
                    Trigg_Desc = request.POST.get('trigg_desc'),
                    Segment_Threshold_1 = request.POST.get('segment_threshold_1'),
                    FLSAvg_Threshold_2 = request.POST.get('flsavg_threshold_2'))
                default_channel_trigg_thres_output.save()
                return render(request, 'threshold_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
                return render(request, 'threshold_success_page.html')

        if form_id == 'Threshold_Logic_Form_edit':
            print('Threshold_Logic_Form_edit')
            try:
                trigger_id = request.POST.get('Trigger_id_Threshold_Logic_Form_edit')
                print("trigger_id:",trigger_id)
                threshold_logic_config = Threshold_Logic_Config.objects.get(trigger_id=trigger_id)

                # Update fields based on the form data
                threshold_logic_config.trigg_desc = request.POST.get('Trigg_Desc_Threshold_Logic_Form_edit')
                threshold_logic_config.thres_description = request.POST.get('Thres_Description_Threshold_Logic_Form_edit')
                threshold_logic_config.thres_query_logic = request.POST.get('Thres_Query_Logic_Threshold_Logic_Form_edit')
                threshold_logic_config.operation = request.POST.get('Operation_Threshold_Logic_Form_edit')
                threshold_logic_config.analysis_period = request.POST.get('Analysis_Period_Threshold_Logic_Form_edit')
                threshold_logic_config.num_thresholds_required = request.POST.get('Num_Threshold_Required_Threshold_Logic_Form_edit')
                threshold_logic_config.segment_threshold_requirement_flag = request.POST.get('Segment_Threshold_1_Requirement_Flag_Threshold_Logic_Form_edit')
                threshold_logic_config.FLS_Threshold_Requirement_Flag = request.POST.get('FLS_Threshold_2_Requirement_Flag_Threshold_Logic_Form_edit')

                threshold_logic_config.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'threshold_success_page.html')
            except Threshold_Logic_Config.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'threshold_success_page.html')
                
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'threshold_success_page.html')

        if form_id == 'Trigger_Threhold_by_Business_Form_edit':
            print('Trigger_Threhold_by_Business_Form_edit')
            try:
                print(request.POST)
                trigger_id = request.POST.get('Trigger_Threhold_by_Business_Form_id')
                print("trigger_id:",trigger_id)
                trigg_Thres_By_Business = Trigg_Thres_By_Business.objects.get(id=trigger_id)
                # Update fields based on the form data
                trigg_Thres_By_Business.Channel = request.POST.get('channel_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.Subchannel = request.POST.get('subchannel_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.Channel_Subchannel_ID = request.POST.get('channel_subchannel_id_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.DemoSeg= request.POST.get('demoseg_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.ValueSeg = request.POST.get('valueseg_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.DemoSeg_ValueSeg_ID = request.POST.get('demoseg_valueseg_id_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.Trigger_id = request.POST.get('trigger_id_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.Trigg_Desc= request.POST.get('trigg_description_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.Segment_Threshold= request.POST.get('segment_threshold_1_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.FLSAvg_Threshold= request.POST.get('flavg_threshold_Trigger_Threhold_by_Business_Form_edit')
                trigg_Thres_By_Business.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'threshold_success_page.html')
            except Trigg_Thres_By_Business.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'threshold_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'threshold_success_page.html')
            


        if form_id == 'Default_Channel_Trigg_thres_Form_Edit':
            print('Default_Channel_Trigg_thres_Form_Edit')
            try:
                # print(request.POST)
                id = request.POST.get('Default_Channel_Trigg_thres_Form_id')
                # print("trigger_id:",trigger_id)
                default_Channel_Trigg_thres = Default_Channel_Trigg_thres.objects.get(id=id)
                # Update fields based on the form data
                default_Channel_Trigg_thres.Channel = request.POST.get('Channel_edit')
                default_Channel_Trigg_thres.Trigger_id = request.POST.get('Trigger_id_edit')
                default_Channel_Trigg_thres.Trigg_Desc = request.POST.get('Trigg_Desc_edit')
                default_Channel_Trigg_thres.Segment_Threshold_1= request.POST.get('Segment_Threshold_1_edit')
                default_Channel_Trigg_thres.FLSAvg_Threshold_2= request.POST.get('FLSAvg_Threshold_2_edit')
                default_Channel_Trigg_thres.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'threshold_success_page.html')
            except Default_Channel_Trigg_thres.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'threshold_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'threshold_success_page.html')
        
        

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
                return render(request, 'closure_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
                return render(request, 'closure_success_page.html')
                    
        if form_id == 'task_closure_Form_edit':
            print('task_closure_Form_edit')
            try:
                trigger_id = request.POST.get('tc_task_id')
                print("trigger_id:",trigger_id)
                threshold_login_config = Task_Closure_Config.objects.get(pk=trigger_id)

                # Update fields based on the form data
                threshold_login_config.Task_Desc = request.POST.get('tc_Task_Desc')
                threshold_login_config.Closure_True_Query = request.POST.get('tc_Closure_True_Query')
                threshold_login_config.Closure_SQL_Query = request.POST.get('tc_closure_sql_query')

                threshold_login_config.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'closure_success_page.html')
            except Threshold_Logic_Config.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'closure_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'closure_success_page.html')
    
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
    queryset_trigger_query_logic = Trigger_ON_Query.objects.all()
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
                return render(request, 'tnt_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
                return render(request, 'tnt_success_page.html')


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
                return render(request, 'tnt_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
                return render(request, 'tnt_success_page.html')


        if form_id == 'trigger_on_query_logic_Form':
            print('trigger_on_query_logic_Form')
            try:
                trigger_on_query_logic = Trigger_ON_Query(
                    Trigger_id = request.POST.get('trigger_id') ,
                    Trigger_Description_Discussed = request.POST.get('trigger_description_discussed'),
                    Assignment_level = request.POST.get('assignment_level'),
                    Iteration_Level = request.POST.get('iteration_level'),
                    Trigger_ON_Query_Logic = request.POST.get('trigger_on_query_logic'),
                    query = request.POST.get('query'))
                trigger_on_query_logic.save()
                messages.success(request, 'Form saved successfully')
                return render(request, 'tnt_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
                return render(request, 'tnt_success_page.html')
                
       
        if form_id == 'channel_task_mapping_Form_edit':
            print('channel_task_mapping_Form_edit')
            try:
                trigger_id = request.POST.get('channel_task_mapping_Form_edit_pk')
                print("trigger_id:",trigger_id)
                channel_task_mapping = Channel_Task_Mapping.objects.get(id=trigger_id)

                # Update fields based on the form data
                channel_task_mapping.Channel = request.POST.get('channel_ctm')
                channel_task_mapping.Channel_Subchannel_ID = request.POST.get('channel_subchannel_id_ctm')
                channel_task_mapping.channel_subchannel_Name = request.POST.get('channel_subchannel_name_ctm')
                channel_task_mapping.DemoSeg_ValueSeg_ID = request.POST.get('demoseg_valueseg_id_ctm')
                channel_task_mapping.DemoSeg_ValueSeg_Name = request.POST.get('demoseg_valueseg_name_ctm')
                channel_task_mapping.Task = request.POST.get('task_ctm')
                channel_task_mapping.save()
                
                messages.success(request, 'Form updated successfully')
                return render(request, 'tnt_success_page.html')
            except Threshold_Logic_Config.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'tnt_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'tnt_success_page.html')
                
                   
        if form_id == 'trigger_on_query_logic_Form_edit':
            print('trigger_on_query_logic_Form_edit')
            try:
                trigger_id = request.POST.get('trigger_id_tql')
                print("trigger_id:", trigger_id)
                trigger_on_query = Trigger_ON_Query.objects.get(Trigger_id =trigger_id)
                trigger_on_query.Trigger_Description_Discussed = request.POST.get('trigger_description_discussed_tql')
                trigger_on_query.Assignment_level = request.POST.get('assignment_level_tql')
                trigger_on_query.Iteration_Level = request.POST.get('iteration_level_tql')
                trigger_on_query.Trigger_ON_Query_Logic = request.POST.get('trigger_on_query_logic_tql')
                trigger_on_query.query  = request.POST.get('query_tql')
                trigger_on_query.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'tnt_success_page.html')
            except Task_Trigger_Mapping.DoesNotExist:
                messages.error(request, 'Record with Task ID {} not found'.format(task_id))
                return render(request, 'tnt_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'tnt_success_page.html')




        if form_id == 'task_trigger_mapping_Form_edit':
            print('task_trigger_mapping_Form_edit')
            try:
                task_id = request.POST.get('task_id_ttm')
                print("task_id:", task_id)
                task_trigger_mapping = Task_Trigger_Mapping.objects.get(Task_id=task_id)
                task_trigger_mapping.Task_Desc = request.POST.get('task_desc_ttm')
                task_trigger_mapping.Task_Stage = request.POST.get('task_stage_ttm')
                task_trigger_mapping.Trigger = request.POST.get('trigger_ttm')
                task_trigger_mapping.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'tnt_success_page.html')
            except Task_Trigger_Mapping.DoesNotExist:
                messages.error(request, 'Record with Task ID {} not found'.format(task_id))
                return render(request, 'tnt_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'tnt_success_page.html')

            
    return render(request, 'TNT.html',context)


def TOAM_Module_View(request):
    # Fetch data for Optimization_Rules
    queryset_optimization_rules = Task_Constraint_Rules.objects.all()
    optimization_rules_df = pd.DataFrame(list(queryset_optimization_rules.values()))
    optimization_rules_headers = list(optimization_rules_df.columns)
    optimization_rules_data = optimization_rules_df.values.tolist()

    # Fetch data for Allocation_Parameters
    queryset_allocation_parameters = Allocation_Parameters.objects.all()
    allocation_parameters_df = pd.DataFrame(list(queryset_allocation_parameters.values()))
    allocation_parameters_headers = list(allocation_parameters_df.columns)
    allocation_parameters_data = allocation_parameters_df.values.tolist()

    # Fetch data for Product_Mix_Focus
    microsegment_default_tasks = Microsegment_Default_Tasks.objects.all()
    microsegment_default_tasks_df = pd.DataFrame(list(microsegment_default_tasks.values()))
    microsegment_default_tasks_headers = list(microsegment_default_tasks_df.columns)
    microsegment_default_tasks_data = microsegment_default_tasks_df.values.tolist()


    context = {
        'optimization_rules_data_headers': optimization_rules_headers,
        'optimization_rules_data_data': optimization_rules_data,
        'allocation_parameters_data_headers': allocation_parameters_headers,
        'allocation_parameters_data_data': allocation_parameters_data,
        'microsegment_default_tasks_data_headers': microsegment_default_tasks_headers,
        'microsegment_default_tasks_data_data': microsegment_default_tasks_data}
    
    if request.method == 'POST':
        print('Django post request')
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)
        if form_id == 'optimization_rules_Form':
            print('optimization_rules_Form') 
            try:  
                optimization_rules = Task_Constraint_Rules(
                    Task_No = request.POST.get('task_no') ,
                    Constraint_Description = request.POST.get('constraint') ,
                    Category_Task_Associated_with =request.POST.get('category_task_allocated_with') ,
                    Min_Task_Count_FLS = request.POST.get('min_task_count_fls') ,
                    Max_Task_Count_FLS = request.POST.get('max_task_count_fls') ,
                    Mutual_Exclusion_Criteria = request.POST.get('mutual_exclusion_criteria') ,
                    Task_Priority =request.POST.get('task_priority') )
                optimization_rules.save()
                messages.success(request, 'Form saved successfully')
                return render(request, 'toam_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)    
                return render(request, 'toam_success_page.html')
        if form_id == 'optimization_rules_Form_edit':
            print('optimization_rules_Form_edit')
            try:
                trigger_id = request.POST.get('ord_task_no')
                print("trigger_id:",trigger_id)
                threshold_login_config = Task_Constraint_Rules.objects.get(Task_No=trigger_id)

                # Update fields based on the form data
                threshold_login_config.Constraint_Description = request.POST.get('ord_constraint')
                threshold_login_config.Category_Task_Associated_with = request.POST.get('ord_category_task_allocated_with')
                threshold_login_config.Min_Task_Count_FLS = request.POST.get('ord_min_task_count_fls')
                threshold_login_config.Max_Task_Count_FLS = request.POST.get('ord_max_task_count_fls')
                threshold_login_config.Mutual_Exclusion_Criteria = request.POST.get('ord_mutual_exclusion_criteria')
                threshold_login_config.Task_Priority = request.POST.get('ord_task_priority')

                threshold_login_config.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'toam_success_page.html')
            except Task_Constraint_Rules.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'toam_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))      
                return render(request, 'toam_success_page.html')  
            
        if form_id == 'allocation_parameters_Form':
            print('allocation_parameters_Form') 
            try:
                allocation_parameters = Allocation_Parameters(
                    Task_id=request.POST.get('task_id'),
                    Channel=request.POST.get('channel'),
                    Subchannel=request.POST.get('subchannel'),
                    DemoSeg=request.POST.get('demoseg'),
                    ValueSeg=request.POST.get('valueseg'),
                    Segment_id=request.POST.get('segment_id'),
                    Due_Days=request.POST.get('due_days'),
                    Buffer_Days=request.POST.get('buffer_days'),
                    XX_Value=request.POST.get('xx_value'),
                    XX_Type=request.POST.get('xx_type'),
                    PricePoint_Reward=request.POST.get('price_point_reward'))
                allocation_parameters.save()
                messages.success(request, 'Form saved successfully')
                return render(request, 'toam_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e) 
                return render(request, 'toam_success_page.html')
            
        if form_id == 'allocation_parameters_Form_edit':
            print('allocation_parameters_Form_edit') 
            try:
                task_id = request.POST.get('AP_Task_id')
                print("task_id:",task_id)
                threshold_login_config = Allocation_Parameters.objects.get(Task_id=task_id)

                # Update fields based on the form data
                threshold_login_config.Channel = request.POST.get('AP_Channel')
                threshold_login_config.Subchannel = request.POST.get('AP_Subchannel')
                threshold_login_config.DemoSeg = request.POST.get('AP_DemoSeg')
                threshold_login_config.ValueSeg = request.POST.get('AP_ValueSeg')
                threshold_login_config.Segment_id = request.POST.get('AP_Segment_id')
                threshold_login_config.Due_Days = request.POST.get('AP_Due_Days')
                threshold_login_config.Buffer_Days = request.POST.get('AP_Buffer_Days')
                threshold_login_config.XX_Value = request.POST.get('AP_XX_Value')
                threshold_login_config.XX_Type = request.POST.get('AP_XX_Type')
                threshold_login_config.PricePoint_Reward = request.POST.get('AP_PricePoint_Reward')
                
                threshold_login_config.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'toam_success_page.html')
                return render(request, 'TOAM.html', context)
            except Task_Constraint_Rules.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'toam_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))     
                return render(request, 'toam_success_page.html')          
                
                
                 
        if form_id == 'microsegment_default_tasks_Form':
            print('microsegment_default_tasks_Form')
            try:
                microsegment_default_tasks = Microsegment_Default_Tasks(
                    Channel = request.POST.get('channel'),
                    Subchannel = request.POST.get('subchannel'),
                    DemoSeg = request.POST.get('demoseg'),
                    ValueSeg = request.POST.get('valueseg'),
                    Segment_id = request.POST.get('segment_id'),
                    Default_Tasks = request.POST.get('default_tasks'))
                microsegment_default_tasks.save()
                messages.success(request, 'Product Mix Focus saved successfully')
                return render(request, 'toam_success_page.html')
            except Exception as e:
                print('Error while saving the data ', e)
                messages.error(request, 'Error while saving the data: {}'.format(str(e)))  
                return render(request, 'toam_success_page.html') 


        if form_id == 'microsegment_default_tasks_Form_edit':
            print('microsegment_default_tasks_Form_edit')
            try:
                id = request.POST.get('mdt_pk_id')
                print("id:", id)
                microsegment_default_tasks = Microsegment_Default_Tasks.objects.get(id=id)

                microsegment_default_tasks.Channel = request.POST.get('channel_mdt')
                microsegment_default_tasks.Subchannel = request.POST.get('subchannel_mdt')
                microsegment_default_tasks.DemoSeg = request.POST.get('demoseg_mdt')
                microsegment_default_tasks.ValueSeg = request.POST.get('valueseg_mdt')
                microsegment_default_tasks.Segment_id = request.POST.get('segment_id_mdt')
                microsegment_default_tasks.Default_Tasks = request.POST.get('default_tasks_mdt')

                microsegment_default_tasks.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'toam_success_page.html')
            except Microsegment_Default_Tasks.DoesNotExist:
                messages.error(request, 'Record with Segment ID {} not found'.format(id))
                return render(request, 'toam_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'toam_success_page.html')


                        

    return render(request, 'TOAM.html',context)


@login_required
def Product_Category_Config_view(request):
    queryset = Product_Category_Config.objects.all()
    Product_Category_Config_df = pd.DataFrame(list(queryset.values()))
    Product_Category_Config_headers = list(Product_Category_Config_df.columns)
    Product_Category_Config_data = Product_Category_Config_df.values.tolist()

    context = {'Product_Category_Config_headers':Product_Category_Config_headers,'Product_Category_Config_data':Product_Category_Config_data }
    # if form_id == 'product_cat_conf_add_form':
    #     print()
    if request.method == 'POST':
        print('Django post request')
        data = request.POST
        form_id = data.get('form_identifier')
        print('data',data)    
        if form_id == 'product_cat_conf_add_form':
            print('product_cat_conf_add_form')
            try:  
                product_category_config = Product_Category_Config(ProductCategoryName=request.POST.get('ProductCategoryName'),
                        FilterQueryOnPolicyTable=request.POST.get('FilterQueryOnPolicyTable'),
                        TrainingTopics=request.POST.get('TrainingTopics'),
                        SellingTaskNo=request.POST.get('SellingTaskNo'),
                        TrainingTaskNo=request.POST.get('TrainingTaskNo')) 
                product_category_config.save()
                messages.success(request, 'Form saved successfully')
                return render(request, 'product_success_page.html')
            except Exception as e:
                print('Error while saving the data ',e)  
                messages.error(request, e)
                return render(request, 'product_success_page.html')
                    
        if form_id == 'product_cat_conf_edit_form':
            print('product_cat_conf_edit_form')
            try:
                trigger_id = request.POST.get('id_edit')
                print("trigger_id:",trigger_id)
                product_category_config = Product_Category_Config.objects.get(pk=trigger_id)

                # Update fields based on the form data
                product_category_config.ProductCategoryName = request.POST.get('ProductCategoryName_edit')
                product_category_config.FilterQueryOnPolicyTable = request.POST.get('FilterQueryOnPolicyTable_edit')
                product_category_config.TrainingTopics = request.POST.get('TrainingTopics_edit')
                product_category_config.SellingTaskNo= request.POST.get('SellingTaskNo_edit')
                product_category_config.TrainingTaskNo= request.POST.get('TrainingTaskNo_edit')
                product_category_config.save()

                messages.success(request, 'Form updated successfully')
                return render(request, 'product_success_page.html')
            except Threshold_Logic_Config.DoesNotExist:
                messages.error(request, 'Record with Trigger ID {} not found'.format(trigger_id))
                return render(request, 'product_success_page.html')
            except Exception as e:
                print('Error while updating the data ', e)
                messages.error(request, 'Error while updating the data: {}'.format(e))
                return render(request, 'product_success_page.html')
    
    return render(request,'Product Category Config.html',context)