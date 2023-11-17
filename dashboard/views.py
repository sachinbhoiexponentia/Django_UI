from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_validation.models import Threshold_Login_Config,Trigg_Thres_By_Business
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

    context = {'Trigg_Thres_By_Business_headers':Trigg_Thres_By_Business_headers,'Threshold_Login_Config_headers': Threshold_Login_Config_headers, 
                  'Threshold_Login_Config_data': Threshold_Login_Config_data,'Trigg_Thres_By_Business_data':Trigg_Thres_By_Business_data}
    return render(request, 'Threshold_logic.html', context)



