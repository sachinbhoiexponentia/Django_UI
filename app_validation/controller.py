import json,ast
import traceback
import pandas as pd
import numpy as np
import sqlparse
import boto3
from io import StringIO
from .models import *


df_config = {}
master_config_json = {
    "allowed_channel":['Agency', 'Banca','Direct','Defence' ],
    "allowed_sub_channel":['BCSS','Defence','Loyalty','DSC'],
    "Allowed_operations" : ['Average','Business','Count','Sum','Manual'],
    "Allowed_Iterations_level":['POLICY', 'LEAD', 'FR', 'APPLICATION', 'OPTIMIZATION_OUTPUT','FLS'],
    "demoSeg_valueSeg_mapping": [
        {
            "DemoSeg":"Urban Lateral Hires",
            "ValueSeg":"Policy Champs",
            "DemoSegid":1,
            "ValueSegid":1
        },
        {
            "DemoSeg":"Seasoned Small Towners",
            "ValueSeg":"Policy Champs",
            "DemoSegid":3,
            "ValueSegid":1
        },
        {
            "DemoSeg":"Small Town Established",
            "ValueSeg":"Middle Joes",
            "DemoSegid":2,
            "ValueSegid":3
         },
         {
            "DemoSeg":"Small Town Established",
            "ValueSeg":"Potentials",
            "DemoSegid":2,
            "ValueSegid":2
         },
         
         
                 {
            "DemoSeg":"Urban Lateral Hires",
            "ValueSeg":"Policy Champs",
            "DemoSegid":'1',
            "ValueSegid":'1'
        },
        {
            "DemoSeg":"Seasoned Small Towners",
            "ValueSeg":"Policy Champs",
            "DemoSegid":'3',
            "ValueSegid":'1'
        },
        {
            "DemoSeg":"Small Town Established",
            "ValueSeg":"Middle Joes",
            "DemoSegid":'2',
            "ValueSegid":'3'
         },
         {
            "DemoSeg":"Small Town Established",
            "ValueSeg":"Potentials",
            "DemoSegid":'2',
            "ValueSegid":'2'
         }
         
    ],
}


S3_BUCKET_NAME = "iearnv2-dev-data"
excel_file_key = "iearnV2-Dev_config_files/Trigg_Thres_by_Business.csv"
 
s3 = boto3.client('s3')

# fetching all trigger ids from 3.c Trigger on query config file 
# valid_trigger_ids = (df_config['Trigger_ON_Query']['Trigger_id']).to_list()
# valid_trigger_ids = [1,2,3,4,46,47,49,13,35,36]
valid_trigger_ids = []
valid_task_ids = []

# valid_task_ids =  (df_config['Task_Trigger_Mapping']['Task_id']).to_list()
# valid_task_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13 (a-j)', '14', '15 (a -j)', '17', '18', '20', '28']

Allowed_operations = ['Average','Business','Count','Sum']

# try:
#     not_allowed_values = Trigg_Thres_by_Business['Channel'][~Trigg_Thres_by_Business['Channel'].isin(master_config_json['allowed_channel'])].tolist()
#     if len(not_allowed_values)>0:
#         print(f"Error: Values {str(list(set(not_allowed_values)))} are not allowed for column channel in sheet Trigg_Thres_by_Business ")
# except Exception as e:
#     print(e)


def validate_sql_query_syntax(sql_query):
    try:
        # parsing the SQL query
        sqlparse.parse(sql_query)
        return True  # No Syntax error if parsed
    except Exception as e:
        # call the sns notification to send to notify the error 
        print(f"there is a syntax error in the query : {e}")
        return False


def validate_sql_query_with_Zero_limit(sql_query):
    try:
        if not validate_sql_query_syntax(sql_query):
            return False

        # database connection
        # excecute sql query with limit 0
        # close the connection
        
        return True
    
    except Exception as e:
        print(str(e))
        return False
        # raise Exception(e)


def data_type_validation(input_value, expected_data_type):
    try:
        if expected_data_type == "int":
            int(input_value)
            
        elif expected_data_type == "float":
            float(input_value)
            
        elif expected_data_type == "str":
            str(input_value)
            
        elif expected_data_type == "bool":
            input_value = input_value.strip().lower()
            if input_value in {"true", "false", "1", "0"}:
                bool(input_value)
            else:
                raise Exception("Invalid value")
        else:
            raise Exception("Unsupported data type")
        
        return True
    except Exception as e:
        print(str(e))
        return False


# used to validate the Threshold_Logic_Config sum of all required threshold 

def ChecK_sum_of_threshold_required(num_threshold_required, segment_threshold, fls_threshold):
    try:
        # check datatype of column 
        if not data_type_validation(num_threshold_required, 'int'):
            return False;
        # checking if sum is valid
        if (int(segment_threshold)+int(fls_threshold)) == int(num_threshold_required):
            return True
        else:
            return False
    
    except Exception as e:
        print(str(e))
        return False



def check_thres_required(input_value):
    try:
        if input_value is np.nan:
            return False
        if int(input_value) != 0 and int(input_value)!=1:
            return False
        return True
    
    except ValueError as e:
        print(str(e))
        return False
    

def Isvalid_demoSegValueSeg(demoseg, valueseg, DemoSeg_ValueSeg_ID):
    try:
        print('master_config_json',master_config_json)
        for obj in master_config_json['demoSeg_valueSeg_mapping']:
            if (
                str(obj['DemoSegid']) == str(demoseg)
                and str(obj['ValueSegid']) == str(valueseg)
                and str(DemoSeg_ValueSeg_ID).lower() == (
                    str(obj['DemoSegid']) + str(obj['ValueSegid'])
                ).lower()
            ):
                return True

        return False

    except Exception as e:
        print(str(e))
        return False








def is_valid_value(value):
    try:
        
        if isinstance(value, (int, float, np.float64, np.int64)):
            return not np.isnan(value)
        
        elif value is not None:
            if isinstance(value, (str, list, dict, set)):
                return bool(value)
            
            elif isinstance(value, object):  # Check for custom objects
                return True
            
        return False
    
    except Exception as e:
        print(str(e))
        return False


# df = df_config['Threshold_Logic_Config']
def checkFlsThresold(thresold, trigger_id,df = None):
    if df is None:
        df = df_config['Threshold_Logic_Config']
    try:
        thresholdRequiredThreshold = df[df["trigger_id"]==trigger_id]['FLS_Threshold_2_Requirement_Flag'].values[0]
        
        if (thresholdRequiredThreshold == int(1)) and is_valid_value(thresold) :
            return True

        return is_valid_value(thresold)
    
    except Exception as e:
        print(str(e))
        return False
        # raise Exception(f" FLS threshold value is not valid. {e}")


        
def validate_thresold_config_df(thresold_config_df = None):

    errors = []
    if thresold_config_df is None:
        thresold_config_df = df_config['Threshold_Logic_Config']
    try:
        validation_flag = True
        
        for i in range(len(thresold_config_df)):
            
            trigger_id =str(thresold_config_df["trigger_id"][i])
            # Check if trigger id is valid 
            print('valid_trigger_ids',valid_trigger_ids)
            print('trigger_id',trigger_id)
            if not is_valid_value(trigger_id) not in valid_trigger_ids:
                validation_flag = False
                errors.append(f"Error in Threshold_Logic_Config for trigger {trigger_id}: trigger id is not valid or empty!!")
            
            sql = thresold_config_df["thres_query_logic"][i]
            # checking if sql query is valid
            if not validate_sql_query_with_Zero_limit(sql):
                validation_flag = False
                errors.append(f"Error in Threshold_Logic_Config for trigger {trigger_id}: The SQL query is not valid") 
                
            # checking if Activation_Flag is valid
            # if not thresold_config_df["Activation_Flag"][i].strip().lower() in {"y", "n", "1", "0"}:
            #     validation_flag = False
            #     errors.append(f"Error in Threshold_Logic_Config for trigger {trigger_id}: invalid Activation_Flag")
            
            # checking if operation is valid 
            print('Allowed_operations',master_config_json['Allowed_operations'])
            if not thresold_config_df["operation"][i] in master_config_json['Allowed_operations']:
                validation_flag = False
                errors.append(f"Error in Threshold_Logic_Config for trigger {trigger_id}: Operation is not allowed.")
            
            # cheking if analysis period is valid it should in integer
        if not is_valid_value(thresold_config_df['analysis_period'][i]) or not data_type_validation(thresold_config_df['analysis_period'][i], 'int') and not data_type_validation(thresold_config_df['analysis_period'][i], 'float'):
            validation_flag = False
            errors.append(f"Error in Threshold_Logic_Config for trigger {trigger_id}: Analysis_Period should be a numeric value.")

            
            # cheking the value of threshold requirement flags for fls or segement and its some
            if check_thres_required(thresold_config_df["segment_threshold_1_requirement_flag"][i]) and check_thres_required(thresold_config_df["fls_threshold_2_requirement_flag"][i]):
                if not ChecK_sum_of_threshold_required(thresold_config_df["num_threshold_required"][i],thresold_config_df["segment_threshold_1_requirement_flag"][i],thresold_config_df["fls_threshold_2_requirement_flag"][i]): 
                    validation_flag = False
                    errors.append(f"Error in Threshold_Logic_Config for in trigger {trigger_id}: The value of Num_thresholds_required is not correct.")
            else:
                validation_flag = False
                errors.append(f"Error in Threshold_Logic_Config for trigger {trigger_id}: The values of columns Segment_Threshold_1_Requirement_Flag and FLS_Threshold_2_Requirement_Flag should be 0 or 1 only ")
            
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        return False, errors + [str(e)+' '+str(i)]


def validate_Trigg_thres_bussness(Trigg_Thres_by_Business = None):
    print('validate_Trigg_thres_bussness',validate_Trigg_thres_bussness)
    
    errors = []
    # try:
    validation_flag = True
    if Trigg_Thres_by_Business is None:
        Trigg_Thres_by_Business = df_config['Trigg_Thres_by_Business'] 
    for i in range(len(Trigg_Thres_by_Business)):
                    
        trigger_id = Trigg_Thres_by_Business['trigger_id'][i]
        
        # check if trigger id is valid or exists in trigger config file 
        print('valid_trigger_ids',valid_trigger_ids)
        print('trigger_id',trigger_id)
        if not is_valid_value(trigger_id) or not trigger_id in valid_trigger_ids: 
            validation_flag = False
            errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: trigger id is not valid or empty!!")
        
        # checking if channel is valid or not
        if not Trigg_Thres_by_Business['channel'][i] in master_config_json['allowed_channel']:
            validation_flag = False
            errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value {Trigg_Thres_by_Business['channel'][i]} for column Channel is  is not allowed.")
        
        # checking if sub_channel is valid or not
        if not Trigg_Thres_by_Business['subchannel'][i] in master_config_json['allowed_sub_channel']:
            validation_flag = False
            errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value {Trigg_Thres_by_Business['subchannel'][i]} for column Subchannel is  is not allowed.")
        
        # checking if the value of demoseg and valueSeg is correct also demoseg valuesegid is valid
        demoseg = Trigg_Thres_by_Business['demoseg'][i]
        ValueSeg = Trigg_Thres_by_Business['valueseg'][i]
        DemoSeg_ValueSeg_ID = Trigg_Thres_by_Business['demoseg_valueseg_id'][i]
        
        if not is_valid_value(demoseg) or not is_valid_value(ValueSeg) or not is_valid_value(DemoSeg_ValueSeg_ID):
            validation_flag = False
            errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value for Demoseg Valueseg and DemoSeg_ValueSeg_ID can't be empty")
        
        # manually commented, uncomment 
        # if not Isvalid_demoSegValueSeg(demoseg, ValueSeg, DemoSeg_ValueSeg_ID):
        #     validation_flag = False
        #     errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value {str([demoseg,ValueSeg,DemoSeg_ValueSeg_ID])} , for column demoseg, valueseg or its id is not correct.")
        # validating the value of segment_threshold_1 is valid integer value
        Trigg_Thres_by_Business['segment_threshold_1'] = int(Trigg_Thres_by_Business['segment_threshold_1'])
        if not isinstance(Trigg_Thres_by_Business['segment_threshold_1'][i], (int, float, np.float64, np.int64)):
            validation_flag = False
            errors.append(f"Errot in Trigg_Thres_by_Business for Trigger {trigger_id}: Segment_Threshold_1 is not correct it should be in integer or float format")
        

    if validation_flag:
        return True, []
    else:
        return False, errors
            
    # except Exception as e: 
        
    #     return False, [str(e)] 
    

def validate_Default_Channel_Trigg_thres(Default_Channel_Trigg_thres = None):
    errors = []
    if Default_Channel_Trigg_thres is None:
        Default_Channel_Trigg_thres = df_config['Default_Channel_Trigg_thres']
    try: 
        validation_flag = True
        for i in range(len(Default_Channel_Trigg_thres)):
            trigger_id = Default_Channel_Trigg_thres['trigger_id'][i]
            
            # check if trigger id is valid or exists in trigger config file 
            if not is_valid_value(trigger_id) or not trigger_id in valid_trigger_ids: 
                validation_flag = False
                errors.append(f"Error in Default_Channel_Trigg_thres for {trigger_id} : trigger id is not valid or empty!!")
            
            # checking if channel is valid or not
            if not Default_Channel_Trigg_thres['Channel'][i] in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Default_Channel_Trigg_thres for trigger {trigger_id}: Value {Default_Channel_Trigg_thres['Channel'][i]} for column Channel is  is not allowed.")
            
            # checking if Segment_Threshold_1 is valie
            if not isinstance(Default_Channel_Trigg_thres['Segment_Threshold_1'][i], (int, float, np.float64, np.int64)):
                validation_flag = False
                errors.append(f"Errot in Default_Channel_Trigg_thres for Trigger {trigger_id}: Segment_Threshold_1 is not correct it should be in integer or float format")
        
             #print(">>>>",checkFlsThresold(Default_Channel_Trigg_thres['Channel'][i],trigger_id))
            
            
        if validation_flag: 
            return True, []
        else:
            return False, errors
            
    except Exception as e: 
        
        return False, [str(e)] 
    
    
def validate_task_constraint_rules(task_constraint_rules = None):
    print('validate_task_constraint_rules')
    errors = []
    # try:
    validation_flag = True
    if task_constraint_rules is None:
        task_constraint_rules = df_config['Task_Constraint_Rules']
    
    for i in range(len(task_constraint_rules)):
        
        task_no = task_constraint_rules["task_no"][i]
        print(task_no)
        task_no = int(task_no)
        print('valid_task_ids',valid_task_ids)
        # Check if task no is valid and present in valid task ids
        if not is_valid_value(task_no) or str(task_no) not in valid_task_ids:
            validation_flag = False
            errors.append(f"Error in Task_Constraint_Rules for task {task_no}: task no is not valid or empty!!")
        
        try:
            val = int(task_constraint_rules["min_task_count_fls"][i])
            print('val',val)
            # Check if Min Task Count/FLS is blank or int between 1 and 5
            if val:
                val = int(val) 
                if  val < 1 or val > 5:
                    validation_flag = False
                    errors.append(f"Error in Task_Constraint_Rules for task {task_no}: Min Task Count/FLS is not valid!")
        except:
            errors.append(f"Min Task Count/FLS should be a number!")
            val = ''

        
        val = task_constraint_rules["max_task_count_fls"][i]
        if val:
            val = int(val)
        # Check if Max Task Count/FLS is blank or int between 1 and 5
            if (not data_type_validation(val, 'int')) or val < 1 or val > 5:
                validation_flag = False
                errors.append(f"Error in Task_Constraint_Rules for task {task_no}: Max Task Count/FLS is not valid!")

        
        # val = list(task_constraint_rules["mutual_exclusion_criteria"][i])
        # print('val',val)
        # if val:
        #     val = int(val)
        # # Check if Mutual Exclusion Criteria is blank or has valid task ids in the list
        #     if set(eval(val)).issubset(set(valid_task_ids)) and not np.isnan(val):
        #         validation_flag = False
        #         errors.append(f"Error in Task_Constraint_Rules for task {task_no}: Mutual Exclusion Criteria is not valid!")
        # try:        
        #     val = int(task_constraint_rules["task_priority"][i])
        # except:
        #     val = ''
        # # Check if task priority is an integer
        # if val:
        #     val = int(val)
        # if not is_valid_value(val) or not data_type_validation(val, 'int'):
        #     validation_flag = False
        #     errors.append(f"Error in Task_Constraint_Rules for task {task_no}: Task Priority is not valid!")
    if validation_flag:
        print(errors, validation_flag)
        return True, []
    else: 
        return False, errors
            
    # except Exception as e: 
    #     return False, [str(e)]

    
def validate_allocation_parameters(allocation_parameters = None):
    errors = []
    try:
        validation_flag = True
        if allocation_parameters is None:
            allocation_parameters = df_config['Allocation_Parameters']
        
        for i in range(len(allocation_parameters)):
            
            task_no = allocation_parameters["task_id"][i]
            # Check if task no is valid and present in valid task ids
            if not is_valid_value(task_no) or str(task_no) not in valid_task_ids:
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: task id is not valid or empty!!")
            
            val = allocation_parameters["channel"][i]
            # Check if channel value is present in allowed channels list
            if val not in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: Channel is not valid!!")
            
            val = allocation_parameters["subchannel"][i]
            # Check if sub channel value is present in allowed sub channels list
            if val not in master_config_json['allowed_sub_channel']:
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: Subchannel is not valid!!")
            
            # Check if the value of demoseg, valueSeg is correct and also demoseg_valuesegid is valid or not
            demoseg = allocation_parameters['demoseg'][i]
            ValueSeg = allocation_parameters['valueseg'][i]
            DemoSeg_ValueSeg_ID = allocation_parameters['segment_id'][i]
            
            if not is_valid_value(demoseg) or not is_valid_value(ValueSeg) or not is_valid_value(DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: Value for Demoseg Valueseg and Segment_id can't be empty")
            
            # if not Isvalid_demoSegValueSeg(demoseg, ValueSeg, DemoSeg_ValueSeg_ID):
            #     validation_flag = False
            #     errors.append(f"Error in Allocation_Parameters for task {task_no}: Value {str([demoseg,ValueSeg,DemoSeg_ValueSeg_ID])} , for column demoseg, valueseg or its id is not correct.")
            
                
            val = allocation_parameters["due_days"][i]
            # Check if trigger id is valid 
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: Due_Days is not valid!")
                
            val = allocation_parameters["buffer_days"][i]
            # Check if trigger id is valid 
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: Buffer Days is not valid!")
                
            val = allocation_parameters["pricepoint_reward"][i]
            # Check if trigger id is valid 
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Allocation_Parameters for task {task_no}: PricePoint(Reward) is not valid!")
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
                
    except Exception as e: 
        return False, [str(e)]
       
        
def validate_microseg_default_tasks(microseg_default_tasks = None):
    errors = []
    try:
        validation_flag = True
        if microseg_default_tasks is None:
            microseg_default_tasks = df_config['Microsegment_Default_Tasks']
        
        for i in range(len(microseg_default_tasks)):
                        
            val = microseg_default_tasks["channel"][i]
            # Check if trigger id is valid 
            if val not in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Channel is not valid!!")
            
            val = microseg_default_tasks["subchannel"][i]
            # Check if trigger id is valid 
            if val not in master_config_json['allowed_sub_channel']:
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Subchannel is not valid!!")
            
            demoseg = microseg_default_tasks['demoseg'][i]
            ValueSeg = microseg_default_tasks['valueseg'][i]
            DemoSeg_ValueSeg_ID = microseg_default_tasks['segment_id'][i]
            
            if not is_valid_value(demoseg) or not is_valid_value(ValueSeg) or not is_valid_value(DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Value for Demoseg Valueseg and Segment_id can't be empty")
            
            # if not Isvalid_demoSegValueSeg(demoseg, ValueSeg, DemoSeg_ValueSeg_ID):
            #     print('demoseg, ValueSeg, DemoSeg_ValueSeg_ID',demoseg, ValueSeg, DemoSeg_ValueSeg_ID)
            #     validation_flag = False
            #     errors.append(f"Error in Microsegement Default Tasks for row {i}: Value {str([demoseg,ValueSeg,DemoSeg_ValueSeg_ID])} , for column demoseg, valueseg or its id is not correct.")
            
            # Default tasks validation to be written    
            
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        return False, [str(e)]


def validate_Task_Closure_Config(Task_Closure_Config_df = None):
    errors = []
    try:
        validation_flag = True
        if Task_Closure_Config_df is None:
            Task_Closure_Config_df = df_config['Task_Closure_Config']
        
        for i in range(len(Task_Closure_Config_df)):
            Task_id = Task_Closure_Config_df['task_id'][i]
            
            # check if TASK id is valid or exists in trigger config file 
            if not is_valid_value(Task_id): # or not str(Task_id) in valid_task_ids:
                validation_flag = False
                errors.append(f"Error in Task_Closure_Config for Task_is {Task_id}: TASK id is not valid or empty!!")
                        
            # checking if the SQL Query for task clouser is valid
            sql = Task_Closure_Config_df["closure_true_query"][i]
            
            # checking if sql query is valid
            if not validate_sql_query_with_Zero_limit(sql):
                validation_flag = False
                errors.append(f"Error in Task_Closure_Config for TaskId {Task_id}: The SQL query is not valid")
                
        if validation_flag: 
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        print(f'Exception: {e}, Traceback:{traceback.format_exc()}')
        return False, [str(e)] 
    
        
def validate_Channel_Task_Mapping(Channel_Task_Mapping = None):
    print('validate_Channel_Task_Mapping')
    errors = []
    try: 
        validation_flag = True
        if Channel_Task_Mapping is None:
            Channel_Task_Mapping = df_config['Channel_Task_Mapping']
        for i in range(len(Channel_Task_Mapping)):
            # checking if channel is valid or not
            print("master_config_json['allowed_channel']",master_config_json['allowed_channel'])
            
            print('Channel',Channel_Task_Mapping['channel'][i])
            if not str(Channel_Task_Mapping['channel'][i].strip()) in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Channel, Channel not is not allowed values.")
            if not Channel_Task_Mapping['subchannel'][i] in master_config_json['allowed_sub_channel']:
                validation_flag = False
                errors.append(f"Error in SubChannel, SubChannel not is not allowed values!")
            # if not Channel_Task_Mapping['channel'][i] in master_config_json['allowed_channel']:
            #     validation_flag = False
            #     errors.append(f"Error in config Channel_Task_Mapping: Value {Channel_Task_Mapping['Channel'][i]} for column Channel is  is not allowed.")
        
            # # checking demoseg_value and its ids
            # DemoSeg_ValueSeg_Name = Channel_Task_Mapping['demoseg_valueseg_name'][i]
            # DemoSeg_ValueSeg_Name = str(DemoSeg_ValueSeg_Name).split("_")
            
            # DemoSeg_ValueSeg_ID = Channel_Task_Mapping['demoseg_valueseg_id'][i]
            # print('len(DemoSeg_ValueSeg_Name)',len(DemoSeg_ValueSeg_Name))
            # if len(DemoSeg_ValueSeg_Name) != 2:
            #     validation_flag = False
            #     errors.append(f"Error in config Channel_Task_Mapping: Value {Channel_Task_Mapping['demoseg_valueseg_name'][i]} for cloumn DemoSeg_ValueSeg_Name is correct it should be seprated by '_' ")
                
            # if not is_valid_value(DemoSeg_ValueSeg_Name[0]) or not is_valid_value(DemoSeg_ValueSeg_Name[1]) or not is_valid_value(DemoSeg_ValueSeg_ID):
            #     validation_flag = False
            #     errors.append("Error in config Channel_Task_Mapping: Value for Demoseg Valueseg and DemoSeg_ValueSeg_ID can't be empty")
            
            # if not Isvalid_demoSegValueSeg(DemoSeg_ValueSeg_Name[0], DemoSeg_ValueSeg_Name[1], DemoSeg_ValueSeg_ID):
            #     validation_flag = False
            #     errors.append(f"Error in config Channel_Task_Mapping: Value {str([DemoSeg_ValueSeg_Name[0], DemoSeg_ValueSeg_Name[1], DemoSeg_ValueSeg_ID])} , for column DemoSeg_ValueSeg_Name, DemoSeg_ValueSeg_ID or its id is not correct.")
            
            # validating the Task Ids 
            # task_ids = Channel_Task_Mapping['task'][i]
            # try:
            #     task_ids = ast.literal_eval(task_ids)
            #     task_ids = [str(tid) for tid in task_ids]
            #     if not isinstance(task_ids, list):
            #         raise ValueError("Task IDs in the Task column are not a valid list.")
            #     if len(set(task_ids)) != len(task_ids):
            #         validation_flag = False
            #         errors.append("Error in config Channel_Task_Mapping: Task column should contain all unique task ids.")
            # except (ValueError, SyntaxError) as e:
            #     validation_flag = False
            #     errors.append('Error in config Channel_Task_Mapping: ' + str(e))
                
            # try:
            #     print('task_ids',task_ids)
            #     print('valid_task_ids',valid_task_ids)
            #     if not set(task_ids).issubset(set(valid_task_ids)):
            #         validation_flag = False
            #         errors.append("Error in config Channel_Task_Mapping: task_ids in Task column are not valid.")
            # except Exception as e:
            #     validation_flag = False
            #     errors.append('Error in config Channel_Task_Mapping: ' + str(e))
                
        if validation_flag: 
            return True, []
        else: 
            return False, errors
            
    except Exception as e:
        return False, errors + [str(e)]




def Validate_Task_Trigger_Mapping(Task_Trigger_Mapping_config=None):
    validation_flag = True
    errors = []

    if Task_Trigger_Mapping_config is None:
        Task_Trigger_Mapping_config = df_config['Task_Trigger_Mapping']

    for i in range(len(Task_Trigger_Mapping_config)):
        task_id = Task_Trigger_Mapping_config['task_id'][i]

        # Check if task id is valid or exists in the trigger config file
        if not is_valid_value(task_id):
            validation_flag = False
            errors.append(f"Error in Task_Trigger_Mapping task {task_id}: task_id is not valid or empty!!")

        # Check if the task stages value is correct
        task_stage = Task_Trigger_Mapping_config['task_stage'][i]
        if not is_valid_value(task_stage):
            validation_flag = False
            errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Task_Stage is not valid or empty!!")

        # Checking if Triggers are valid in mapping
        jsonval = Task_Trigger_Mapping_config['trigger'][i]
        print('jsonval',jsonval)
        if not is_valid_value(jsonval):
            validation_flag = False
            errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Trigger column is not valid or empty!!")

        Trigger = None
        invalid_column = False


        # {35:M} not valid
        # try:
        #     # Use json.loads to convert the string to a dictionary
        #     Trigger = ast.literal_eval(jsonval)
        # except json.JSONDecodeError as e:
        #     invalid_column = True
        #     validation_flag = False
        #     errors.append(f"Error in Task_Trigger_Mapping task {task_id}: the format of Trigger column is not valid. {str(e)}")

        # if not invalid_column:
        #     for trigger_id in Trigger:
        #         # Checking if key is a valid trigger id and values are either 'O' or 'M'
        #         trigger_value = Trigger[trigger_id]
        #         if trigger_value.upper() not in ['O', 'M']:
        #             validation_flag = False
        #             errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Trigger column contains invalid value {trigger_value}!!")

        #         if int(trigger_id) not in valid_trigger_ids:
        #             errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Trigger column contains invalid trigger id {trigger_id}!!")

    return validation_flag, errors


def validate_Trigger_ON_Query(Trigger_ON_Query = None):
    print('validate_Trigger_ON_Query',validate_Trigger_ON_Query)
    errors = []
    try: 
        validation_flag = True
        if Trigger_ON_Query is None:
            Trigger_ON_Query = df_config['Trigger_ON_Query']
        
        for i in range(len(Trigger_ON_Query)):
            trigger_id = int(Trigger_ON_Query['trigger_id'][i])
            
            # check if trigger id is valid or exists in trigger config file 
            if not is_valid_value(trigger_id) or not isinstance(trigger_id, (int, float, np.float64, np.int64)):
                validation_flag = False
                errors.append(f"Error in Trigger_ON_Query for Trigger {trigger_id}: trigger id is not valid or empty!!")
            
            # check if value Num_Threshold_required
            # Num_Threshold_required = Trigger_ON_Query['num_threshold_required'][i]
            # if not is_valid_value(Num_Threshold_required) or Num_Threshold_required not in [1,0,2]:
            #     validation_flag = False
            #     errors.append(f"Errot in Trigger_ON_Query for Trigger {trigger_id}: Num_Threshold_required is not valid or empty, it should be numeric value either 1,2,or 0!!")
            
            
            sql = Trigger_ON_Query['trigger_on_query_logic'][i]
            
            # checking if sql query for trigger is valid or not
            if not validate_sql_query_with_Zero_limit(sql):
                validation_flag = False
                errors.append(f"Error in Trigger_ON_Query for trigger {trigger_id}: The SQL query is not valid") 
            
            
        if validation_flag: 
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        
        return False, [str(e)] 


def product_cat_conf_add_form(product_category_df):
    return True, []


config_sheets= {
                #Threshold
                'Threshold_Logic_Form':validate_thresold_config_df,
                'Trigger_Threhold_by_Business_Form':validate_Trigg_thres_bussness,
                'Threshold_Logic_Form_edit':validate_thresold_config_df,
                'Trigger_Threhold_by_Business_Form_edit':validate_Trigg_thres_bussness,
                # Closure
                'closure_form':validate_Task_Closure_Config,
                'task_closure_Form':validate_Task_Closure_Config,
                # TNT
                'channel_task_mapping_Form':validate_Channel_Task_Mapping,
                'task_trigger_mapping_Form':Validate_Task_Trigger_Mapping,
                'trigger_on_query_logic_Form':validate_Trigger_ON_Query,
                'channel_task_mapping_Form_edit':validate_Channel_Task_Mapping,
                'task_trigger_mapping_Form_edit':Validate_Task_Trigger_Mapping,
                'trigger_on_query_logic_Form_edit':validate_Trigger_ON_Query,
                # TOAM
                'task_constraint_rules_Form':validate_task_constraint_rules,
                'allocation_parameters_Form':validate_allocation_parameters,
                'microsegment_default_tasks_Form':validate_microseg_default_tasks,
                'task_constraint_rules_Form_edit':validate_task_constraint_rules,
                'allocation_parameters_Form_edit':validate_allocation_parameters,
                'microsegment_default_tasks_Form_edit':validate_microseg_default_tasks,
                
                'Default_Channel_Trigg_thres':validate_Default_Channel_Trigg_thres,# not used
                'product_cat_conf_add_form':product_cat_conf_add_form
                }
 

def mainValidate_function(sheet_name = None, data_df = None):
    global df_config, valid_trigger_ids, valid_task_ids
    try:
        # obj = s3.get_object(Bucket= S3_BUCKET_NAME, Key=f"iearnV2-Dev_config_files/{sheet}.csv")
        # df_config.update({sheet:pd.read_csv(obj['Body'])})
        # queryset = Threshold_Logic_Config.objects.all()
        # Threshold_Logic_Config_df = pd.DataFrame(list(queryset.values()))
        # queryset = Trigg_Thres_By_Business.objects.all()
        # Trigg_Thres_By_Business_df = pd.DataFrame(list(queryset.values()))
        # queryset = Default_Channel_Trigg_thres.objects.all()
        # Default_Channel_Trigg_thres_df = pd.DataFrame(list(queryset.values()))
        # queryset = Task_Closure_Config.objects.all()
        # Task_Closure_Config_df = pd.DataFrame(list(queryset.values()))
        # queryset = Channel_Task_Mapping.objects.all()
        # Channel_Task_Mapping_df = pd.DataFrame(list(querysfet.values()))
        queryset = Task_Trigger_Mapping.objects.all()
        Task_Trigger_Mapping_df = pd.DataFrame(list(queryset.values()))
        queryset = Trigger_ON_Query.objects.all()
        Trigger_ON_Query_df = pd.DataFrame(list(queryset.values()))
        # queryset = Task_Constraint_Rules.objects.all()
        # Task_Constraint_Rules_df = pd.DataFrame(list(queryset.values()))
        # queryset = Allocation_Parameters.objects.all()
        # Allocation_Parameters_df = pd.DataFrame(list(queryset.values()))
        # queryset = Microsegment_Default_Tasks.objects.all()
        # Microsegment_Default_Tasks_df = pd.DataFrame(list(queryset.values()))
    except:
        print("error ",sheet)
    valid_trigger_ids = Trigger_ON_Query_df['Trigger_id'].to_list()
    valid_task_ids = Task_Trigger_Mapping_df['Task_id'].to_list()
    
    isValid_config = True
    allerror = {}
    if sheet_name:
        isValid_config, allerror = config_sheets[sheet_name](data_df)
    else:
        for sheet in config_sheets.keys():
            status, error = config_sheets[sheet]()
            isValid_config = isValid_config and status
            allerror.update({sheet:error})
    return isValid_config, allerror


def s3_upload(data_df,sheet_name,s3_bucket,s3_path):
    try:
        # obj = s3.get_object(Bucket= s3_bucket, Key=s3_path+f"{sheet_name}.csv")
        # main_df = pd.read_csv(obj['Body'])
        # main_df = main_df.append(data_df).reset_index(drop=True)
        csv_buffer = StringIO()
        data_df.to_csv(csv_buffer)
        s3.put_object(Bucket=s3_bucket,Key=s3_path+f"{sheet_name}.csv",Body=csv_buffer.get_value())
        return True, 'Data upload sucess.'
    except Exception as e:
        return False, str(e)
