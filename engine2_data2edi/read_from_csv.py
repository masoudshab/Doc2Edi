import json
import collections
import os
import glob
import csv
from datetime import datetime
from dateutil.parser import parse


# Get the current working directory
# cwd = os.getcwd()

# Navigate to the parent directory
# parent_dir = os.path.dirname(cwd)

# Navigate to a subdirectory inside the parent directory
data_dir = os.path.join('C:\\OKO\\Doc2Edi\\data_assets')

print(data_dir)

        
edi_field_map = {
    'sender_id': {
        "keywords": ['sender_id', 'sender', 'send', 'id', 'ref'], # : '123456',
        "data_type_rules": ["whitespace-free"],
    },
    'receiver_id': {
        "keywords": ['receiver_id', 'receiver', 'receiv', 'id', 'ref'], # : '123456',
        "data_type_rules": ["whitespace-free"],
    },
    'shipper': {
        "keywords": ['shipper', 'shipper_name', 'carrier_name', 'carrier'], # : 'ACME Trucking',
        "data_type_rules": ["isalpha"],
    },
    'shipper_id': {
        "keywords": ['shipper_id', 'shipper_ref', 'carrier_id', 'id', 'carrier'], # : 'ACME Trucking',
        "data_type_rules": ["whitespace-free"],
    },
    'shipment_id': {
        "keywords": ['shipment_id', 'reference', 'file_number', 'ref'],  # '123456',
        "data_type_rules": ["whitespace-free"],
    },
    'origin_city': {
        "keywords": ['origin_city', 'pickup_city', 'pickup_location', 'org', 'city'],  # 'Chicago',
        "data_type_rules": ["isalpha"],
    },
    'origin_state': {
        "keywords": ['origin_state', 'pickup_state', 'pickup_location', 'org', 'state'],  # 'IL',
        "data_type_rules": ["two-letter-state-code"],
    },
    'origin_zip': {
        "keywords": ['origin_zip', 'zip', 'postal'],  
        "data_type_rules": ["isnumber"],
    },
    'destination_city': {
        "keywords": ['delivery_city', 'destination_city', 'destination', 'dest', 'city'],  # 'Dallas',
        "data_type_rules": ["isalpha"],
    },
    'destination_state': {
        "keywords": ['delivery_state', 'destination_state', 'destination', 'dest', 'state'],  # 'TX',
        "data_type_rules": ["two-letter-state-code"],
    },
    'destination_zip': {
        "keywords": ['destination_zip', 'zip', 'postal'], 
        "data_type_rules": ["isnumber"],
    },
    'pickup_date': {
        "keywords": ['pickup_date', 'pickup_time', 'pickup_datetime', 'date', 'time'],  # datetime.date(2023, 5, 8),
        "data_type_rules": ["datetime"],
    },
    'delivery_date': {
        "keywords": ['delivery_time', 'delivery_datetime', 'delivery_date', 'date', 'time'],  # datetime.date(2023, 5, 15),
        "data_type_rules": ["datetime"],
    },
    'total_weight': {
        "keywords": ['weight'],  # 5000,
        "data_type_rules": ["isnumber"],
    },
    'total_volume': {
        "keywords": ['volume', ],  # 200,
        "data_type_rules": ["isnumber"],
    },
    'total_pieces': {
        "keywords": ['pieces', 'quantity', 'qty'],  # 100
        "data_type_rules": ["isdigit"],
    },
    'instructions': {
        "keywords": ['instruction'],
        "data_type_rules": [],
    },
    'requirements': {
        "keywords": ['requirement'],
        "data_type_rules": [],
    },
    'bill': {
        "keywords": ['bill'],
        "data_type_rules": [],
    },
    'contact_info': {
        "keywords": ['contact', 'address', 'phone'],
        "data_type_rules": [],
    },
    'value': {
        "keywords": ['value'],
        "data_type_rules": [],
    },
    'interchange_control_number': {
        "keywords": ['interchange', 'control', 'number'],
        "data_type_rules": ["isnumber"],
    },
    'group_control_number': {
        "keywords": ['group', 'control', 'number'],
        "data_type_rules": ["isnumber"],
    },
    'transaction_control_number': {
        "keywords": ['transaction', 'control', 'number'],
        "data_type_rules": ["isnumber"],
    },
    'freight_charge': {
        "keywords": ['freight', 'charge', 'fee'],
        "data_type_rules": ["isnumber"],
    },
    'consignee_name':{
        "keywords": ['consignee_name', 'consignee', 'consig'],
        "data_type_rules": ["isalpha"],
    },
    'consignee_id':{
        "keywords": ['consignee_id', 'consignee', 'consig', 'number', 'ref', 'id'],
        "data_type_rules": ["isnumber"],
    },
}

def findEdiField(edi_field, json_file):
    """
    For example if "edi_field" is "shipper":
    "shipper": Name of the shipper or carrier.
    keywords = ['shipper', 'shipper_name', 'carrier_name', 'carrier']
    example: 'ACME Trucking'
    """
    edi_field_found_items = collections.defaultdict(list)

    for field_name_from_file, field_value_from_file in json_file.items():
        field_name = field_name_from_file.lower().replace(" ", "_").replace(":", "").replace("#", "")

        for i, key in enumerate(edi_field_map[edi_field]["keywords"]):
            if key in field_name:
                key_dict = {"imp": i,
                            "key": key,
                            "field_name_from_file": field_name_from_file,
                            "field_name": field_name,
                            "field_value_from_file": field_value_from_file,
                            "edi_field": edi_field
                            }
                edi_field_found_items[field_name].append(key_dict)
    
    return edi_field_found_items


def processEdiInfo(edi_field, json_file):
    edi_field_found_items = findEdiField(json_file, edi_field)

    if len(edi_field_found_items) == 0:
        return None

    imp = float("infinity")
    field_name_from_file = ""
    field_value_from_file = ""

    for field_name, key_dict_list in edi_field_found_items.items():
        for key_dict in key_dict_list:
            if key_dict["imp"] < imp:
                imp = key_dict["imp"]
                field_name_from_file = key_dict["field_name_from_file"]
                field_value_from_file = key_dict["field_value_from_file"]
            elif key_dict["imp"] == imp:
                field_name_from_file = field_name_from_file + "   &&&   " + key_dict["field_name_from_file"]
                field_value_from_file = field_value_from_file + "   &&&   " + key_dict["field_value_from_file"]
    
    edi_field_best_item = {
        "field_name_from_file": field_name_from_file,
        "field_value_from_file": field_value_from_file
    }

    return edi_field_best_item


def dataTypeCheckDatetime(string, format="%Y-%m-%d %H:%M:%S"):
    """
    "data_type_rule" = 'datetime'
    return: 
        is_valid: T/F
        is_processed: T/F
        output_string: formatted_string if is_processed else string
    """
    # first try: Parse the date string dynamically in general format
    is_valid = False
    try:
        date_object = parse(string)
        formatted_string = date_object.strftime("%Y-%m-%d %H:%M:%S")
        is_valid = True
        # print("first try is successful!")
    except ValueError:
        pass    

    # second try: Parse the date string dynamically with input_format
    try:
        date_object = datetime.strptime(string, format)
        formatted_string = date_object.strftime("%Y-%m-%d %H:%M:%S")
        is_valid = True
        # print("second try is successful!")
    except ValueError:
        pass
    
    if is_valid:
        return True, True, formatted_string
    else:
        return False, False, string

# date_string = "Apr/21/2023"
# dataTypeCheckDatetime(date_string)


def dataTypeCheckIsAlpha(string):
    """
    "data_type_rule" = 'isalpha'
    return: 
        is_valid: T/F
        is_processed: T/F
        output_string: formatted_string if is_processed else string
    """
    if string.replace(" ", "").replace(".", "").isalpha():
        is_valid = True
    else:
        is_valid = False

    return is_valid, False, string

# string = "POLYMEM S.A"
# dataTypeCheckIsAlpha(string)


def dataTypeCheckIsNumber(string, format="float"):
    """
    "data_type_rule" = 'isnumber' or 
                       'isdigit' when format="int"
    return: 
        is_valid: T/F
        is_processed: T/F
        output_string: formatted_string if is_processed else string
    """
    # first try: Parse the string as int
    is_valid = False
    is_digit = False
    is_float = False
    
    try:
        integer_value = int(string)
        is_digit = True
        # print("first try is successful!")
    except ValueError:
        pass    

    # second try: Parse the string as float
    try:
        float_value = float(string)
        is_float = True
        # print("second try is successful!")
    except ValueError:
        pass
    
    if format=="int" and is_digit:
        return True, True, str(integer_value)
    elif is_float:
        return True, True, str(float_value)
    elif is_digit:
        return True, True, str(integer_value)
    else:
        return False, False, string
    
# string = "123"
# dataTypeCheckIsNumber(string, format="int")

def dataTypeCheckWhiteSpaceFree(string):
    """
    "data_type_rule" = 'whitespace-free'
    return: 
        is_valid: T/F
        is_processed: T/F
        output_string: formatted_string if is_processed else string
    """
    if not string.isspace() and ' ' not in string:
        is_valid = True
    else:
        is_valid = False

    return is_valid, False, string


def dataTypeCheckTwoLetterStateCode(string):
    """
    "data_type_rule" = 'two-letter-state-code'
    return: 
        is_valid: T/F
        is_processed: T/F
        output_string: formatted_string if is_processed else string
    """
    # List of valid two-letter state codes
    valid_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
                   'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
                   'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
                   'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                   'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    is_valid = False
    is_processed = False

    # Check if input_string is in the list of valid codes
    if string.upper() in valid_codes:
        is_valid = True
    else:
        for substr in string.split(" "):
            if substr.upper() in valid_codes:
                is_valid = True
                is_processed = True
                formatted_string = substr.upper()
                break
    
    return is_valid, is_processed, formatted_string if is_processed else string.upper() 

# string = "BRITISH AIRWAYS p.l.c\n200 Crofton BLDG 5 West Access Rd., Kenner, LA 70062"
# dataTypeCheckTwoLetterStateCode(string)
    

def dataTypeCheck(edi_field, field_val):
    """
    "data_type_rules": set of rules that define data types of different "edi_field"s
    "data_type_rules" can be one of the bellow defined rules:
    {'datetime',
    'isalpha',
    'isdigit',
    'isnumber',
    'two-letter-state-code',
    'whitespace-free'}

    return:     
        is_valid: T/F
        is_processed: T/F
        output_string: formatted_string if is_processed else string
    """
    data_type_rules_result = {}
    data_type_rules = edi_field_map[edi_field]["data_type_rules"]
    for data_type_rule in data_type_rules:
        if data_type_rule == "datetime":
            data_type_rules_result[data_type_rule] = dataTypeCheckDatetime(field_val)
        elif data_type_rule == "isalpha":
            data_type_rules_result[data_type_rule] = dataTypeCheckIsAlpha(field_val)
        elif data_type_rule == "isdigit":
            data_type_rules_result[data_type_rule] = dataTypeCheckIsNumber(field_val, format="int")
        elif data_type_rule == "isnumber":
            data_type_rules_result[data_type_rule] = dataTypeCheckIsNumber(field_val)
        elif data_type_rule == "two-letter-state-code":
            data_type_rules_result[data_type_rule] = dataTypeCheckTwoLetterStateCode(field_val)
        elif data_type_rule == "whitespace-free":
            data_type_rules_result[data_type_rule] = dataTypeCheckWhiteSpaceFree(field_val)
    
    return data_type_rules_result

def convertToValidValues(edi_field, edi_field_best_item):
    if not edi_field_best_item:
        return None
    
    field_value_from_file = edi_field_best_item["field_value_from_file"]

    # this is where there are "multiple fields" in the file for one edi_field
    if "   &&&   " in field_value_from_file:
        for field_value in field_value_from_file.split("   &&&   "):
            data_type_rules_result = dataTypeCheck(edi_field, field_value)
            for data_type_rule, result in data_type_rules_result.items():
                if result[0] and len(result[2]) > len(edi_field_best_item.get("valid_field_value", "")):
                    edi_field_best_item[f"dq_check__{data_type_rule}"] = result[0]
                    edi_field_best_item["data_is_processed"] = True
                    edi_field_best_item["valid_field_value"] = result[2]
    
    # this is where there are "long strings" with ", "
    elif ", " in field_value_from_file:
        for field_value in field_value_from_file.split(", "):
            data_type_rules_result = dataTypeCheck(edi_field, field_value)
            for data_type_rule, result in data_type_rules_result.items():
                if result[0] and len(result[2]) > edi_field_best_item.get("valid_field_value", 0):
                    edi_field_best_item[f"dq_check__{data_type_rule}"] = result[0]
                    edi_field_best_item["data_is_processed"] = True
                    edi_field_best_item["valid_field_value"] = result[2]

    else:
        data_type_rules_result = dataTypeCheck(edi_field, field_value_from_file)
        for data_type_rule, result in data_type_rules_result.items():
            edi_field_best_item[f"dq_check__{data_type_rule}"] = result[0]
            if result[1]:
                edi_field_best_item["data_is_processed"] = result[1]
            if result[0]:
                edi_field_best_item["valid_field_value"] = result[2]
    
    return edi_field_best_item

# TODO: 0
# correct the directory to data_asset
# for dictionary, use .get() instead of []
# change this python file name frm read_from_csv


# TODO-1: 
# "Pickup:": "Wednesday, May 3, 2023 3:00 PM-5:00 PM", 
# "Pickup Location:": "BRITISH AIRWAYS p.l.c\n200 Crofton BLDG 5 West Access Rd., Kenner, LA 70062",
# "Pickup Instructions": "PICKUP DATE/TIME 5/3/2023 15:00\nCLOSE TIME 17:00",

# TODO-2: Delivery Due Date is confused by pickup_date in files[2]  --> instead it can be easily found in the instructions "Pickup Instructions": "PICKUP DATE/TIME 5/3/2023 15:00\nCLOSE TIME 17:00"
# pickup_date
# {
#     "field_name_from_file": "Delivery Due Date",
#     "field_value_from_file": "5/9/2023",
#     "dq_check__datetime": true,
#     "data_is_processed": true,
#     "valid_field_value": "2023-05-09 00:00:00"
# }
# instructions
# {
#     "field_name_from_file": "Pickup Instructions",
#     "field_value_from_file": "PICKUP DATE/TIME 5/3/2023 15:00\nCLOSE TIME 17:00"
# }

# TODO-3:
# total_weight
# {
#     "field_name_from_file": "WEIGHT   &&&   VOL WEIGHT",
#     "field_value_from_file": "845.00 Kg\n1,862.91 Lb   &&&   CLASS70"
# }

def buildEDI211(shipment_data):
    isa_segment = f"ISA*00**00**08*{shipment_data['sender_id']}*14*{shipment_data['receiver_id']}*{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*U*00401*{shipment_data['interchange_control_number']}*0*P*>"
    gs_segment = f"GS*BL*{shipment_data['sender_id']}*{shipment_data['receiver_id']}*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*{shipment_data['group_control_number']}*X*004010"
    st_segment = f"ST*211*{shipment_data['transaction_control_number']}"
    b10_segment = f"B10*{shipment_data['shipment_id']}*{shipment_data['total_weight']}****{shipment_data['freight_charge']}**{shipment_data['pickup_date']}*{shipment_data['shipment_id']}*{shipment_data['shipper_id']}"
    n1_sh_segment = f"N1*SH*{shipment_data['shipper']}*92*{shipment_data['shipper_id']}"
    n1_sf_segment = f"N1*SF*{shipment_data['shipper']}*92*{shipment_data['shipper_id']}"
    n1_cn_segment = f"N1*CN*{shipment_data['consignee_name']}*92*{shipment_data['consignee_id']}"
    n4_oy_segment = f"N4*OY*{shipment_data['origin_city']}*{shipment_data['origin_state']}*{shipment_data['origin_zip']}"
    n4_de_segment = f"N4*DE*{shipment_data['destination_city']}*{shipment_data['destination_state']}*{shipment_data['destination_zip']}"
    g62_pd_segment = f"G62*10*{shipment_data['pickup_date']}"
    g62_dd_segment = f"G62*14*{shipment_data['delivery_date']}"
    se_segment = f"SE*10*{shipment_data['transaction_control_number']}"
    ge_segment = f"GE*1*{shipment_data['group_control_number']}"
    
    edi_211 = f"{isa_segment}\n{gs_segment}\n{st_segment}\n{b10_segment}\n{n1_sh_segment}\n{n1_sf_segment}\n{n1_cn_segment}\n{n4_oy_segment}\n{n4_de_segment}\n{g62_pd_segment}\n{g62_dd_segment}\n{se_segment}\n{ge_segment}\n"
    return edi_211





# Iterate through all files in the directory with a .json extension and run Engine 2's components in squential way (DAG pipeline)
processed_files = {}

for file in glob.glob(os.path.join(data_dir, "*.json")):
    # print(file)
    with open(file, "r") as f:
        print(f"opened {file} ...... ")
        json_data = json.load(f)

        edi_fields = {} 
        for edi_field in edi_field_map:
            edi_field_best_item = processEdiInfo(json_data, edi_field)
            edi_field_best_item = convertToValidValues(edi_field, edi_field_best_item)
            if edi_field_best_item and "valid_field_value" in edi_field_best_item and edi_field_best_item["valid_field_value"]:
                edi_fields[edi_field] = edi_field_best_item["valid_field_value"]
                print(f"valid_field_value for {edi_field}: ", edi_fields[edi_field])
            elif edi_field_best_item and "field_value_from_file" in edi_field_best_item and edi_field_best_item["field_value_from_file"]:
                edi_fields[edi_field] = edi_field_best_item["field_value_from_file"]
                print(f"field_value_from_file for {edi_field}: ", edi_fields[edi_field])
            else:
                edi_fields[edi_field] = f"not_found_{edi_field}"
                print(f"not_found_{edi_field}: ", edi_fields[edi_field])

        print(json.dumps(edi_fields, indent=4))
        print(f"Successfully converted data from {file} to EDI format ...... ")
        print("      ")
        edi_211 = buildEDI211(shipment_data=edi_fields)
        print(edi_211)
        # processed_files[file] = edi_fields
    
    file_name = file.split("\\")[-1].split(".")[0]
    # with open(, "w") as f:
    #     json.dump(edi_211, fp, indent=4)
    #     import csv

    # Open a CSV file in write mode
    with open(f'{file_name}_edi_211.csv', mode='w', newline='') as csv_file:
        
        # Create a CSV writer object
        writer = csv.writer(csv_file)
        
        # Split the string into lines
        lines = edi_211.split('\n')
        
        # Iterate over the lines and write each line as a list
        for line in lines:
            writer.writerow([line])

