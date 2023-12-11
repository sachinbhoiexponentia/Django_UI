# models.py in your app_validation app

from django.db import models


class Threshold_Logic_Config(models.Model):
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
    

class Default_Channel_Trigg_thres(models.Model):
    Channel = models.CharField(max_length=50)
    Trigger_id = models.IntegerField()
    Trigg_Desc = models.TextField()
    Segment_Threshold_1 = models.IntegerField()
    FLSAvg_Threshold_2 = models.IntegerField()

    def __str__(self):
        return f"Channel:{self.Channel} - Trigger_id:{self.Trigger_id} - Trigg_Desc:{self.Trigg_Desc} - Segment_Threshold_1: {self.Segment_Threshold_1} - FLSAvg_Threshold_2: {self.FLSAvg_Threshold_2}" 
    

class Task_Closure_Config(models.Model):
    Task_id = models.CharField(primary_key=True, max_length=50)
    Task_Desc = models.CharField(max_length=255)
    Closure_True_Query = models.TextField()
    Closure_SQL_Query=models.TextField()

    def __str__(self):
        return f"{self.Task_id} - {self.Task_Desc}"
       
       
class Channel_Task_Mapping(models.Model):
    Channel = models.CharField(max_length=50)
    Subchannel = models.CharField(max_length=50)
    DemoSeg = models.CharField(max_length=10)
    ValueSeg = models.CharField(max_length=10)
    Task = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.Channel} - {self.Subchannel}"
    
    
class Task_Trigger_Mapping(models.Model):
    Task_id = models.CharField(primary_key=True,max_length=50)
    Task_Desc = models.CharField(max_length=255)
    Task_Stage = models.CharField(max_length=50)
    Trigger = models.JSONField()

    def __str__(self):
        return f"{self.Task_id} - {self.Task_Desc} - {self.Task_Stage}"



class Trigger_ON_Query(models.Model):
    Trigger_id = models.IntegerField(primary_key=True)
    Trigger_Description_Discussed = models.TextField()
    Assignment_level = models.CharField(max_length=50)
    Iteration_Level = models.CharField(max_length=50)
    Trigger_ON_Query_Logic = models.TextField()
    query = models.TextField()

    def __str__(self):
        return f"{self.Trigger_id} - {self.Trigger_Description_Discussed} - {self.Assignment_level} - {self.Iteration_Level}"
    
    
    
class Task_Constraint_Rules(models.Model):
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


class Microsegment_Default_Tasks(models.Model):
    Channel = models.CharField(max_length=100)
    Subchannel = models.CharField(max_length=100)
    DemoSeg =models.FloatField(null=True, blank=True)
    ValueSeg = models.FloatField(null=True, blank=True)
    Segment_id = models.FloatField(null=True, blank=True)
    Default_Tasks = models.TextField()
    
    def __str__(self):
        return f"{self.Channel} - {self.Subchannel} - {self.DemoSeg} - {self.ValueSeg} - {self.Segment_id} - {self.Default_Tasks}"
    

class Product_Category_Config(models.Model):
    ProductCategoryName=models.CharField(max_length=100)
    FilterQueryOnPolicyTable=models.CharField(max_length=100)
    TrainingTopics=models.CharField(max_length=100)
    SellingTaskNo=models.CharField(max_length=100)
    TrainingTaskNo=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.ProductCategoryName} - {self.FilterQueryOnPolicyTable} - {self.TrainingTopics} - {self.SellingTaskNo} - {self.TrainingTaskNo}"