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
