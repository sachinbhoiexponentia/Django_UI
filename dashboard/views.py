from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_validation.models import Threshold_Login_Config,Trigg_Thres_By_Business,Segment_Threshold_Output,FLS_Avg_Threshold_Output,Task_Closure_Config
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
    print(Segment_Threshold_Output_df)
    Segment_Threshold_Output_headers = list(Segment_Threshold_Output_df.columns)
    Segment_Threshold_Output_data = Segment_Threshold_Output_df.values.tolist()

    queryset3 = FLS_Avg_Threshold_Output.objects.all()
    FLS_Avg_Threshold_Output_df = pd.DataFrame(list(queryset3.values()))
    print(FLS_Avg_Threshold_Output_df )
    FLS_Avg_Threshold_Output_headers = list(FLS_Avg_Threshold_Output_df.columns)
    FLS_Avg_Threshold_Output_data = FLS_Avg_Threshold_Output_df.values.tolist()

    context = {'FLS_Avg_Threshold_Output_headers':FLS_Avg_Threshold_Output_headers,'FLS_Avg_Threshold_Output_data':FLS_Avg_Threshold_Output_data ,'Segment_Threshold_Output_data':Segment_Threshold_Output_data,
              'Segment_Threshold_Output_headers':Segment_Threshold_Output_headers,'Trigg_Thres_By_Business_headers':Trigg_Thres_By_Business_headers,'Threshold_Login_Config_headers': Threshold_Login_Config_headers, 
            'Threshold_Login_Config_data': Threshold_Login_Config_data,'Trigg_Thres_By_Business_data':Trigg_Thres_By_Business_data}
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
def TNT_Module_view(request):
    return render(request, 'TNT.html')