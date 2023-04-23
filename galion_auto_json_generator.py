
# clear ; python3 galion_auto_json_generator.py GALION_LALINET_CEILAPOZONE_TEMPLATE.json ../licel_files/ ./JSON_OUT/
# clear ; python3 galion_auto_json_generator.py GALION_NDACC_MLO_TEMPLATE.json ../licel_files/ ./JSON_OUT/

import json
import sys
import os
import re

if len(sys.argv) == 4:

    if ( os.path.isfile( sys.argv[1]) ) and ( os.path.isdir( sys.argv[2]) ):

        # READ THE FILES INSIDE THE FOLDER CONTAINING THE LIDAR DATA, SKIP THE FOLDERS -------------------
        file_list = [ f for f in os.listdir(sys.argv[2]) if os.path.isfile(os.path.join(sys.argv[2], f)) ] 

        # FILTER THE FILES THAT NOT CONTAINS NUMBERS IN THE EXTENSION ------------------------------------
        file_list = [ f for f in file_list if re.search(r'\d+', os.path.splitext(f)[1] ) ]

        # DEFINE AN BOOLEAN ARRAY WITH THE AVAILABLE DATA (ALL FALSE BY DEFAULT)
        hours_with_Data = [False for i in range(24)]

        # SET 'TRUE' IN hours_with_Data IF THERE IS A LICEL FILE ACQUIRED IN THAT HOUR
        for file_name in file_list:
            hours_with_Data[ int(file_name[6:8]) ] = True

        # READ THE JSON FILE TEMPLATE TO LOAD THE GENERAL INFORMATION OF THE SITE ----------------------------------------------------------------------------------------------------------- 
        with open(sys.argv[1], 'r') as file:
            data = json.load(file)

        # UPDATE THE DATE BASED ON WHAT WAS READ IN THE FIRST FILE IN THE INPUT LICEL FOLDER
        data['date'] = f"{2000+int(file_list[0][1:3])}-{int(file_list[0][3:4], 16):02d}-{int(file_list[0][4:6]):02d}" 

        # UPDATE "true" OR "false" IN "available" VARIABLE BASED ON WHAT WAS READ IN THE INPUT FOLDER (ARGUMENT NUMBER 2)
        # print( f"len(data['data']): {len(data['data']): }" )
        for d in range( len(data['data']) ):
            data['data'][d]['available'][:] = hours_with_Data
            # data['data'][d]['status'][:] = 

        # WRITE THE OUTPUT JSON FILE -----------------------------------------------------------------------------------------------------------
        output_json_file = f"{sys.argv[3]}{os.path.basename(sys.argv[1])}"
        file_name_date = f"{2000+int(file_list[0][1:3])}{int(file_list[0][3:4], 16):02d}{int(file_list[0][4:6]):02d}"

        output_json_file = output_json_file.replace("TEMPLATE", file_name_date)
        with open( output_json_file, "w") as file:
            json.dump(data, file, indent=4)

    else: # if ( os.path.isfile( sys.argv[1]) ) and ( os.path.isdir( sys.argv[2]) ):
        print("Wrong usage of the arguments: Usage:\n\t galion_auto_json_generator.json full_path_to_json_template_file full_path_to_LICEL_files_FOLDER full_path_to_output_json_file")

else: # if len(sys.argv) == 3:
    print( f"Wrong number of arguments. Usage:\n\t galion_auto_json_generator.json full_path_to_json_template_file full_path_to_LICEL_files_FOLDER full_path_to_output_json_file")


