# models.py in your app_validation app

from django.db import models

class Threshold_Login_Config(models.Model):
    trigger_id = models.IntegerField(primary_key=True)
    trigg_desc = models.TextField()
    thres_description = models.TextField()
    thres_query_logic = models.TextField()
    operation = models.CharField(max_length=50)
    analysis_period = models.CharField(max_length=50,null=True, blank=True)
    num_thresholds_required = models.IntegerField()
    segment_threshold_requirement_flag = models.FloatField(null=True, blank=True) # null values are not allowed in int field, so had to use float
    FLS_Threshold_Requirement_Flag = models.FloatField(null=True, blank=True)  # null values are not allowed in int field, so had to use float

    def __str__(self):
        return f"Trigger ID: {self.trigger_id}, Description: {self.trigg_desc}"



class Trigg_Thres_By_Business(models.Model):
    Channel = models.CharField(max_length=50)
    Subchannel = models.CharField(max_length=50)
    Channel_Subchannel_ID = models.IntegerField()
    DemoSeg = models.CharField(max_length=50)
    ValueSeg = models.CharField(max_length=50)
    DemoSeg_ValueSeg_ID = models.IntegerField()
    Trigger_id = models.IntegerField()
    Trigg_Desc = models.CharField(max_length=255)
    Segment_Threshold = models.IntegerField()
    FLSAvg_Threshold = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.Channel} - {self.Subchannel} - {self.Trigger_id} - {self.Trigg_Desc}"
    
    
    
class Segment_Threshold_Output(models.Model):
    Channel = models.CharField(max_length=50)
    Subchannel = models.CharField(max_length=50)
    Channel_Subchannel_ID = models.IntegerField()
    DemoSeg = models.IntegerField()
    ValueSeg = models.IntegerField()
    DemoSeg_ValueSeg_ID = models.IntegerField()
    Trigger_id = models.IntegerField()
    Segment_Threshold = models.IntegerField()

    def __str__(self):
        return f"{self.Channel} - {self.Subchannel} - {self.Trigger_id} - DemoSeg: {self.DemoSeg} - ValueSeg: {self.ValueSeg} - Segment_Threshold: {self.Segment_Threshold}"
    
    
    
class FLS_Avg_Threshold_Output(models.Model):
    FLS_id = models.IntegerField(primary_key=True)
    Channel = models.CharField(max_length=50)
    Subchannel = models.CharField(max_length=50)
    Channel_Subchannel_ID = models.IntegerField()
    DemoSeg = models.IntegerField()
    ValueSeg = models.IntegerField()
    DemoSeg_ValueSeg_ID = models.IntegerField()
    Trigger_id = models.IntegerField()
    FLSAvg_Threshold = models.IntegerField()

    def __str__(self):
        return f"{self.FLS_id} - {self.Channel} - {self.Subchannel} - {self.Trigger_id} - DemoSeg: {self.DemoSeg} - ValueSeg: {self.ValueSeg} - FLSAvg_Threshold: {self.FLSAvg_Threshold}" 
    
    
       
       
class Task_Closure_Config(models.Model):
    Task_id = models.IntegerField(primary_key=True)
    Task_Desc = models.CharField(max_length=255)
    Closure_True_Query = models.TextField()

    def __str__(self):
        return f"{self.Task_id} - {self.Task_Desc}"
       
       
class Channel_Task_Mapping(models.Model):
    Channel = models.CharField(max_length=50)
    Channel_Subchannel_ID = models.IntegerField()
    channel_subchannel_Name = models.CharField(max_length=50)
    DemoSeg_ValueSeg_ID = models.IntegerField()
    DemoSeg_ValueSeg_Name = models.CharField(max_length=255)
    Task = models.JSONField()

    def __str__(self):
        return f"{self.Channel} - {self.Channel_Subchannel_ID} - {self.channel_subchannel_Name}"
    
    
class Task_Trigger_Mapping(models.Model):
    Task_id = models.CharField(primary_key=True,max_length=50)
    Task_Desc = models.CharField(max_length=255)
    Task_Stage = models.CharField(max_length=50)
    Trigger = models.JSONField()

    def __str__(self):
        return f"{self.Task_id} - {self.Task_Desc} - {self.Task_Stage}"



class Trigger_ON_Query_Logic(models.Model):
    Trigger_id = models.IntegerField(primary_key=True)
    Trigger_Description_Discussed = models.TextField()
    Assignment_level = models.CharField(max_length=50)
    Iteration_Level = models.CharField(max_length=50)
    Trigger_ON_Query_Logic = models.TextField()
    query = models.TextField()

    def __str__(self):
        return f"{self.Trigger_id} - {self.Trigger_Description_Discussed} - {self.Assignment_level} - {self.Iteration_Level}"
    
    
    
class Optimization_Rules(models.Model):
    Task_No = models.CharField(primary_key=True,max_length=50)
    Constraint_Description = models.TextField()
    Category_Task_Associated_with = models.CharField(max_length=100)
    Min_Task_Count_FLS = models.FloatField(null=True, blank=True)
    Max_Task_Count_FLS = models.FloatField(null=True, blank=True)
    Mutual_Exclusion_Criteria = models.TextField()
    Task_Priority = models.IntegerField()

    def __str__(self):
        return f"{self.Task_No} - {self.Constraint_Description} - {self.Category_Task_Associated_with} - {self.Min_Task_Count_FLS} - {self.Max_Task_Count_FLS} - {self.Mutual_Exclusion_Criteria} - {self.Task_Priority}"
    
    
    
    
    
class Allocation_Parameters(models.Model):
    Task_id = models.CharField(primary_key=True,max_length=50)
    Channel = models.CharField(max_length=100)
    Subchannel = models.CharField(max_length=100)
    DemoSeg = models.FloatField(null=True, blank=True)
    ValueSeg = models.FloatField(null=True, blank=True)
    Segment_id = models.FloatField(null=True, blank=True)
    Due_Days = models.FloatField(null=True, blank=True)
    Buffer_Days = models.FloatField(null=True, blank=True)
    XX_Value = models.CharField(max_length=100, blank=True)
    XX_Type = models.CharField(max_length=100, blank=True)
    PricePoint_Reward = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.Task_id} - {self.Channel} - {self.Subchannel} - {self.DemoSeg} - {self.ValueSeg} - {self.Segment_id} - {self.Due_Days} - {self.Buffer_Days} - {self.XX_Value} - {self.XX_Type} - {self.PricePoint_Reward}"
    
class Product_Mix_Focus(models.Model):
    Channel = models.CharField(max_length=100)
    Subchannel = models.CharField(max_length=100)
    DemoSeg =models.FloatField(null=True, blank=True)
    ValueSeg = models.FloatField(null=True, blank=True)
    Focus_Product = models.CharField(max_length=100)
    prod_mix_non_par_annuity_immediate = models.FloatField(null=True, blank=True)
    prod_mix_non_par_c2p = models.FloatField(null=True, blank=True)
    prod_mix_non_par_sanchay = models.FloatField(null=True, blank=True)
    prod_mix_non_par_annuity_pgp = models.FloatField(null=True, blank=True)
    prod_mix_non_par_health = models.FloatField(null=True, blank=True)
    prod_mix_par_others = models.FloatField(null=True, blank=True)
    prod_mix_par_ppt_10 = models.FloatField(null=True, blank=True)
    prod_mix_ul_others = models.FloatField(null=True, blank=True)
    prod_mix_ul_ppt_10 =models.FloatField(null=True, blank=True)
    prod_mix_ul_single_pre = models.FloatField(null=True, blank=True)
    class Meta:
        # Composit key
        unique_together = ('Channel', 'Subchannel', 'DemoSeg', 'ValueSeg', 'Focus_Product')

    def __str__(self):
        return f"{self.Channel} - {self.Subchannel} - {self.DemoSeg} - {self.ValueSeg} - {self.Focus_Product}"    
    
            