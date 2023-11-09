import json
import pandas as pd
import numpy as np
import sqlparse
import boto3


df_config = {}
master_config_json = {
    "allowed_channel":['Agency', 'Banca','Direct' ],
    "allowed_sub_channel":['BCSS','Defence','Loyalty','DSC'],
    "Allowed_operations" : ['Average','Business','Count','Sum'],
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


# used to validate the Threshold Logic Config sum of all required threshold 

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
    

def Isvalid_demoSegValueSeg(demoseg, valueseg,DemoSeg_ValueSeg_ID):
    try:
        if type(demoseg) == np.int64:
            demoseg = list(filter(lambda x : x['DemoSegid']==demoseg,master_config_json['demoSeg_valueSeg_mapping'])).pop()['DemoSeg']
            valueseg = list(filter(lambda x : x['ValueSegid']==valueseg,master_config_json['demoSeg_valueSeg_mapping'])).pop()['ValueSeg']
        for obj in master_config_json['demoSeg_valueSeg_mapping']:
            if obj['DemoSeg'].lower() == demoseg.lower() and obj['ValueSeg'].lower() == valueseg.lower() and str(DemoSeg_ValueSeg_ID).lower() == (str(obj['DemoSegid']) + str(obj['ValueSegid'])).lower():
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


def checkFlsThresold(thresold, trigger_id):
    try:
        thresholdRequiredThreshold = df_config['Threshold Logic Config'][df_config['Threshold Logic Config']["Trigger_id"]==trigger_id]['FLS_Threshold_2_Requirement_Flag'].values[0]
        
        if (thresholdRequiredThreshold == int(1)) and is_valid_value(thresold) :
            return True

        return is_valid_value(thresold)
    
    except Exception as e:
        print(str(e))
        return False
        # raise Exception(f" FLS threshold value is not valid. {e}")


        
def validate_thresold_config_df():
    errors = []
    try:
        validation_flag = True

        thresold_config_df= df_config['Threshold Logic Config']
        
        for i in range(len(thresold_config_df)):
            
            trigger_id =thresold_config_df["Trigger_id"][i]
            # Check if trigger id is valid 
            if not is_valid_value(trigger_id) or trigger_id not in valid_trigger_ids:
                validation_flag = False
                errors.append(f"Error in Threshold Logic Config for trigger {trigger_id}: trigger id is not valid or empty!!")
            
            sql = thresold_config_df["sql_Thres_Query_Logic"][i]
            # checking if sql query is valid
            if not validate_sql_query_with_Zero_limit(sql):
                validation_flag = False
                errors.append(f"Error in Threshold Logic Config for trigger {trigger_id}: The SQL query is not valid") 
                
            # checking if Activation_Flag is valid
            if not thresold_config_df["Activation_Flag"][i].strip().lower() in {"y", "n", "1", "0"}:
                validation_flag = False
                errors.append(f"Error in Threshold Logic Config for trigger {trigger_id}: invalid Activation_Flag")
            
            # checking if operation is valid 
            if not thresold_config_df["Operation"][i] in master_config_json['Allowed_operations']:
                validation_flag = False
                errors.append(f"Error in Threshold Logic Config for trigger {trigger_id}: Operation is not allowed.")
            
            # cheking if analysis period is valid it should in integer
            if not is_valid_value(thresold_config_df['Analysis_Period'][i]) or not data_type_validation(thresold_config_df['Analysis_Period'][i], 'int'):
                validation_flag = False
                errors.append(f"Error in Threshold Logic Config for trigger {trigger_id}: Analysis_Period should be an integer value.")
            
            # cheking the value of threshold requirement flags for fls or segement and its some
            if check_thres_required(thresold_config_df["Segment_Threshold_1_Requirement_Flag"][i]) and check_thres_required(thresold_config_df["FLS_Threshold_2_Requirement_Flag"][i]):
                if not ChecK_sum_of_threshold_required(thresold_config_df["Num_thresholds_required"][i],thresold_config_df["Segment_Threshold_1_Requirement_Flag"][i],thresold_config_df["FLS_Threshold_2_Requirement_Flag"][i]): 
                    validation_flag = False
                    errors.append(f"Error in Threshold Logic Config for in trigger {trigger_id}: The value of Num_thresholds_required is not correct.")
            else:
                validation_flag = False
                errors.append(f"Error in Threshold Logic Config for trigger {trigger_id}: The values of columns Segment_Threshold_1_Requirement_Flag and FLS_Threshold_2_Requirement_Flag should be 0 or 1 only ")
            
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        return False, errors + [str(e)+' '+str(i)]


def validate_Trigg_thres_bussness():
    
    errors = []
    try:
        validation_flag = True
        Trigg_Thres_by_Business = df_config['Trigg_Thres_by_Business'] 
        for i in range(len(Trigg_Thres_by_Business)):
                        
            trigger_id = Trigg_Thres_by_Business['Trigger_id'][i]
            
            # check if trigger id is valid or exists in trigger config file 
            if not is_valid_value(trigger_id) or not trigger_id in valid_trigger_ids: 
                validation_flag = False
                errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: trigger id is not valid or empty!!")
            
            # checking if channel is valid or not
            if not Trigg_Thres_by_Business['Channel'][i] in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value {Trigg_Thres_by_Business['Channel'][i]} for column Channel is  is not allowed.")
            
            # checking if sub_channel is valid or not
            if not Trigg_Thres_by_Business['Subchannel'][i] in master_config_json['allowed_sub_channel']:
                validation_flag = False
                errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value {Trigg_Thres_by_Business['Subchannel'][i]} for column Subchannel is  is not allowed.")
            
            # checking if the value of demoseg and valueSeg is correct also demoseg valuesegid is valid
            demoseg = Trigg_Thres_by_Business['DemoSeg'][i]
            ValueSeg = Trigg_Thres_by_Business['ValueSeg'][i]
            DemoSeg_ValueSeg_ID = Trigg_Thres_by_Business['DemoSeg_ValueSeg_ID'][i]
            
            if not is_valid_value(demoseg) or not is_valid_value(ValueSeg) or not is_valid_value(DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value for Demoseg Valueseg and DemoSeg_ValueSeg_ID can't be empty")
            
            if not Isvalid_demoSegValueSeg(demoseg, ValueSeg, DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Trigg_Thres_by_Business for trigger {trigger_id}: Value {str([demoseg,ValueSeg,DemoSeg_ValueSeg_ID])} , for column demoseg, valueseg or its id is not correct.")
            # validating the value of segment_threshold_1 is valid integer value
            if not isinstance(Trigg_Thres_by_Business['Segment_Threshold_1'][i], (int, float, np.float64, np.int64)):
                validation_flag = False
                errors.append(f"Errot in Trigg_Thres_by_Business for Trigger {trigger_id}: Segment_Threshold_1 is not correct it should be in integer or float format")
            

        if validation_flag:
            return True, []
        else:
            return False, errors
            
    except Exception as e: 
        
        return False, [str(e)] 
    

def validate_Default_Channel_Trigg_thres():
    errors = []
    Default_Channel_Trigg_thres = df_config['Default_Channel_Trigg_thres']
    try: 
        validation_flag = True
        for i in range(len(Default_Channel_Trigg_thres)):
            trigger_id = Default_Channel_Trigg_thres['Trigger_id'][i]
            
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
    
    
def validate_task_constraint_rules():
    errors = []
    try:
        validation_flag = True
        thresold_config_df= df_config['Task Constraint Rules']
        
        for i in range(len(thresold_config_df)):
            
            task_no = thresold_config_df["Task No"][i]
            # Check if task no is valid and present in valid task ids
            if not is_valid_value(task_no) or str(task_no) not in valid_task_ids:
                validation_flag = False
                errors.append(f"Error in Task Constraint Rules for task {task_no}: task no is not valid or empty!!")
            
            val = thresold_config_df["Min Task Count/FLS"][i]
            # Check if Min Task Count/FLS is blank or int between 1 and 5
            if (not np.isnan(val) and not data_type_validation(val, 'int')) or val<1 or val>5:
                validation_flag = False
                errors.append(f"Error in Task Constraint Rules for task {task_no}: Min Task Count/FLS is not valid!")
            
            val = thresold_config_df["Max Task Count/FLS"][i]
            # Check if Max Task Count/FLS is blank or int between 1 and 5
            if (not np.isnan(val) and not data_type_validation(val, 'int')) or val<1 or val>5:
                validation_flag = False
                errors.append(f"Error in Task Constraint Rules for task {task_no}: Max Task Count/FLS is not valid!")
            
            val = thresold_config_df["Mutual Exclusion Criteria"][i]
            # Check if Mutual Exclusion Criteria is blank or has valid task ids in the list
            if not(type(val)==str and set(eval(val)).issubset(set(valid_task_ids))) and not np.isnan(val):
                validation_flag = False
                errors.append(f"Error in Task Constraint Rules for task {task_no}: Mutual Exclusion Criteria is not valid!")
                
            val = thresold_config_df["Task Priority"][i]
            # Check if task priority is an integer
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Task Constraint Rules for task {task_no}: Task Priority is not valid!")
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        return False, [str(e)]

    
def validate_allocation_parameters():
    errors = []
    try:
        validation_flag = True
        thresold_config_df= df_config['Allocation Parameters']
        
        for i in range(len(thresold_config_df)):
            
            task_no = thresold_config_df["Task_id"][i]
            # Check if task no is valid and present in valid task ids
            if not is_valid_value(task_no) or str(task_no) not in valid_task_ids:
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: task id is not valid or empty!!")
            
            val = thresold_config_df["Channel"][i]
            # Check if channel value is present in allowed channels list
            if val not in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: Channel is not valid!!")
            
            val = thresold_config_df["Subchannel"][i]
            # Check if sub channel value is present in allowed sub channels list
            if val not in master_config_json['allowed_sub_channel']:
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: Subchannel is not valid!!")
            
            # Check if the value of demoseg, valueSeg is correct and also demoseg_valuesegid is valid or not
            demoseg = thresold_config_df['DemoSeg'][i]
            ValueSeg = thresold_config_df['ValueSeg'][i]
            DemoSeg_ValueSeg_ID = thresold_config_df['Segment_id'][i]
            
            if not is_valid_value(demoseg) or not is_valid_value(ValueSeg) or not is_valid_value(DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: Value for Demoseg Valueseg and Segment_id can't be empty")
            
            if not Isvalid_demoSegValueSeg(demoseg, ValueSeg, DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: Value {str([demoseg,ValueSeg,DemoSeg_ValueSeg_ID])} , for column demoseg, valueseg or its id is not correct.")
            
                
            val = thresold_config_df["Due_Days"][i]
            # Check if trigger id is valid 
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: Due_Days is not valid!")
                
            val = thresold_config_df["Buffer Days"][i]
            # Check if trigger id is valid 
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: Buffer Days is not valid!")
                
            val = thresold_config_df["PricePoint(Reward)"][i]
            # Check if trigger id is valid 
            if not is_valid_value(val) or not data_type_validation(val, 'int'):
                validation_flag = False
                errors.append(f"Error in Allocation Parameters for task {task_no}: PricePoint(Reward) is not valid!")
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        return False, [str(e)]
       
        
def validate_microseg_default_tasks(df = None):
    errors = []
    try:
        validation_flag = True
        thresold_config_df= df_config['Microsegment Default Tasks']
        
        for i in range(len(thresold_config_df)):
                        
            val = thresold_config_df["Channel"][i]
            # Check if trigger id is valid 
            if val not in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Channel is not valid!!")
            
            val = thresold_config_df["Subchannel"][i]
            # Check if trigger id is valid 
            if val not in master_config_json['allowed_sub_channel']:
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Subchannel is not valid!!")
            
            demoseg = thresold_config_df['DemoSeg'][i]
            ValueSeg = thresold_config_df['ValueSeg'][i]
            DemoSeg_ValueSeg_ID = thresold_config_df['Segment_id'][i]
            
            if not is_valid_value(demoseg) or not is_valid_value(ValueSeg) or not is_valid_value(DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Value for Demoseg Valueseg and Segment_id can't be empty")
            
            if not Isvalid_demoSegValueSeg(demoseg, ValueSeg, DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in Microsegement Default Tasks for row {i}: Value {str([demoseg,ValueSeg,DemoSeg_ValueSeg_ID])} , for column demoseg, valueseg or its id is not correct.")
            
            # Default tasks validation to be written    
            
        if validation_flag:
            print(errors, validation_flag)
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        return False, [str(e)]


def validate_Task_Closure_Config():
    errors = []
    try:
        validation_flag = True
        Task_Closure_Config_df = df_config['Task_Closure_Config']
        
        for i in range(len(Task_Closure_Config_df)):
            Task_id = Task_Closure_Config_df['Task_id'][i]
            
            # check if TASK id is valid or exists in trigger config file 
            if not is_valid_value(Task_id) or not str(Task_id) in valid_task_ids:
                validation_flag = False
                errors.append(f"Error in Task_Closure_Config for Task_is {Task_id}: TASK id is not valid or empty!!")
                        
            # checking if the SQL Query for task clouser is valid
            sql = Task_Closure_Config_df["Closure_True_Query"][i]
            
            # checking if sql query is valid
            if not validate_sql_query_with_Zero_limit(sql):
                validation_flag = False
                errors.append(f"Error in Task_Closure_Config for TaskId {Task_id}: The SQL query is not valid")
                
        if validation_flag: 
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        
        return False, [str(e)] 
    
        
def validate_Channel_Task_Mapping():
    errors = []
    try: 
        validation_flag = True
        Channel_Task_Mapping = df_config['Channel_Task_Mapping']
        for i in range(len(Channel_Task_Mapping)):
            
            # checking if channel is valid or not
            if not Channel_Task_Mapping['Channel'][i] in master_config_json['allowed_channel']:
                validation_flag = False
                errors.append(f"Error in config Channel_Task_Mapping: Value {Channel_Task_Mapping['Channel'][i]} for column Channel is  is not allowed.")
        
            # checking demoseg_value and its ids
            DemoSeg_ValueSeg_Name = Channel_Task_Mapping['DemoSeg_ValueSeg_Name'][i]
            DemoSeg_ValueSeg_Name = str(DemoSeg_ValueSeg_Name).split("_")
            DemoSeg_ValueSeg_ID = Channel_Task_Mapping['DemoSeg_ValueSeg_ID'][i]
            
            if len(DemoSeg_ValueSeg_Name) != 2:
                validation_flag = False
                errors.append(f"Error in config Channel_Task_Mapping: Value {Channel_Task_Mapping['DemoSeg_ValueSeg_Name'][i]} for cloumn DemoSeg_ValueSeg_Name is correct it should be seprated by '_' ")
                
            if not is_valid_value(DemoSeg_ValueSeg_Name[0]) or not is_valid_value(DemoSeg_ValueSeg_Name[1]) or not is_valid_value(DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append("Error in config Channel_Task_Mapping: Value for Demoseg Valueseg and DemoSeg_ValueSeg_ID can't be empty")
            
            if not Isvalid_demoSegValueSeg(DemoSeg_ValueSeg_Name[0], DemoSeg_ValueSeg_Name[1], DemoSeg_ValueSeg_ID):
                validation_flag = False
                errors.append(f"Error in config Channel_Task_Mapping: Value {str([DemoSeg_ValueSeg_Name[0], DemoSeg_ValueSeg_Name[1], DemoSeg_ValueSeg_ID])} , for column DemoSeg_ValueSeg_Name, DemoSeg_ValueSeg_ID or its id is not correct.")
            
            # validating the Task Ids 
            # task_ids = json.loads(Channel_Task_Mapping['Task'][i])
            try:
                task_ids = eval(Channel_Task_Mapping['Task'][i])
                if len(set(task_ids)) != len(task_ids):
                    validation_flag = False
                    errors.append("Error in config Channel_Task_Mapping: TAsk  column should contains all the unique task ids.")
            except Exception as e:
                validation_flag = False
                errors.append('Error in config Channel_Task_Mapping: '+ str(e))
                
            if not set(task_ids).issubset(set(valid_task_ids)):
                validation_flag = False
                errors.append("Error in config Channel_Task_Mapping: task_ids in TAsk column is not valid.")
                
        if validation_flag: 
            return True, []
        else: 
            return False, errors
            
    except Exception as e:
        return False, errors + [str(e)]

def Validate_Task_Trigger_Mapping():
    errors = []
    Task_Trigger_Mapping_config = df_config['Task_Trigger_Mapping']
    
    try: 
        validation_flag = True
        for i in range(len(Task_Trigger_Mapping_config)):
            
            task_id = Task_Trigger_Mapping_config['Task_id'][i]
            
            # check if task id is valid or exists in trigger config file 
            if not is_valid_value(task_id):
                validation_flag = False
                errors.append(f"Error in Task_Trigger_Mapping task {task_id}: task_id is not valid or empty!!")
      
            # checking if the task statges value is correct 
            #allowed_task_Stages = ['Lead Conversion - Pre Login', 'Lead Conversion - Post Login', 'Combo Task', 'Overall Sales', 'Renewal', 'Training Task', 'Lead Generation', 'Lead Conversion - Pre Login', 'Lead Conversion - Post Login']
            
            # need to ask ravi do we need to check only allowed values or only empty check
            
            if not is_valid_value(Task_Trigger_Mapping_config['Task_Stage']):
                validation_flag = False
                errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Task_Stage is not valid or empty!!")
                
            #checking if Triggers are valid in mapping 
            
            jsonval = Task_Trigger_Mapping_config['Trigger'][i]
            
            if not is_valid_value(jsonval):
                validation_flag = False
                errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Trigger column  is not valid or empty!!")
            
            Trigger = None
            invalid_coumn = False
            if isinstance(jsonval, str):
                try:
                    Trigger = json.loads(jsonval)
                except json.JSONDecodeError as e:
                    invalid_coumn  = True
                    validation_flag = False
                    errors.append(f"Error in Task_Trigger_Mapping task {task_id}: the format of Trigger column is not valid. {str(e)}")
            elif isinstance(jsonval, object):
                Trigger = jsonval
            else:
                invalid_coumn = True 
                validation_flag = False
                errors.append(f"Error in Task_Trigger_Mapping task {task_id}: the format of Trigger column is not valid")
            
            if not invalid_coumn:
                for trigger_id in Trigger:
                    # checking if key is valid trigger id and values is either optional or manadatery
                    if not Trigger[trigger_id].lower() in ['o','m']:
                        validation_flag = False
                        errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Trigger clolumn contains invalid value {Trigger[trigger_id]} !!")
                    
                    if not int(trigger_id) in valid_trigger_ids:
                        errors.append(f"Error in Task_Trigger_Mapping task {task_id}: Trigger clolumn contains invalid trigger id {trigger_id} !!")

        if validation_flag: 
            return True, []
        else: 
            return False, errors
            
    except Exception as e: 
        
        return False, [str(e)] 


def validate_Trigger_ON_Query():
    errors = []
    try: 
        validation_flag = True
        Trigger_ON_Query = df_config['Trigger_ON_Query']
        
        for i in range(len(Trigger_ON_Query)):
            trigger_id = Trigger_ON_Query['Trigger_id'][i]
            
            # check if trigger id is valid or exists in trigger config file 
            if not is_valid_value(trigger_id) or not isinstance(trigger_id, (int, float, np.float64, np.int64)):
                validation_flag = False
                errors.append(f"Errot in Trigger_ON_Query for Trigger {trigger_id}: trigger id is not valid or empty!!")
            
            # check if value Num_Threshold_required
            Num_Threshold_required = Trigger_ON_Query['Num_Threshold_required'][i]
            if not is_valid_value(Num_Threshold_required) or Num_Threshold_required not in [1,0,2]:
                validation_flag = False
                errors.append(f"Errot in Trigger_ON_Query for Trigger {trigger_id}: Num_Threshold_required is not valid or empty, it should be numeric value either 1,2,or 0!!")
            
            
            sql = Trigger_ON_Query['Trigger_ON_Query_Logic'][i]
            
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


config_sheets= {
                'Threshold Logic Config':validate_thresold_config_df,
                'Trigg_Thres_by_Business':validate_Trigg_thres_bussness,
                'Default_Channel_Trigg_thres':validate_Default_Channel_Trigg_thres,
                'Channel_Task_Mapping':validate_Channel_Task_Mapping,
                'Task_Trigger_Mapping':Validate_Task_Trigger_Mapping,
                'Task_Closure_Config':validate_Task_Closure_Config,
                'Trigger_ON_Query':validate_Trigger_ON_Query,
                'Task Constraint Rules':validate_task_constraint_rules,
                'Allocation Parameters':validate_allocation_parameters,
                'Microsegment Default Tasks':validate_microseg_default_tasks}


def mainValidate_function():
    global df_config, valid_trigger_ids, valid_task_ids
    for sheet in config_sheets.keys():
        try:
            obj = s3.get_object(Bucket= S3_BUCKET_NAME, Key=f"iearnV2-Dev_config_files/{sheet}.csv")
            df_config.update({sheet:pd.read_csv(obj['Body'])})
        except:
            print("error ",sheet)
    valid_trigger_ids = (df_config['Trigger_ON_Query']['Trigger_id']).to_list()
    valid_task_ids =  (df_config['Task_Trigger_Mapping']['Task_id']).to_list()
    
    isValid_config = True
    allerror = {}
    for sheet in config_sheets.keys():
        status, error = config_sheets[sheet]()
        isValid_config = isValid_config and status
        allerror.update({sheet:error})
    return isValid_config, allerror
