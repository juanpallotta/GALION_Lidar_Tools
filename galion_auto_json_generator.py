
# clear ; python3 galion_auto_json_generator.py GALION_LALINET_CEILAPOZONE_TEMPLATE_OPERATIONAL.json ../licel_files/20150425/ ./JSON_OUT/

# clear ; python3 galion_auto_json_generator.py GALION_LALINET_CEILAPOZONE_TEMPLATE_OPERATIONAL.json /mnt/Disk-1_8TB/Argentina/test/20190906/ ./JSON_OUT/

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

        # DEFINE THE ARRAYS TO FILL WIHT THE NEW DATA
        data_available = [False for i in range(24)]
        data_status    = ["na"  for i in range(24)]

        # READ THE JSON FILE TEMPLATE TO LOAD THE GENERAL INFORMATION OF THE SITE ----------------------------------------------------------------------------------------------------------- 
        with open(sys.argv[1], 'r') as file:
            data_template = json.load(file)

        # UPDATE THE DATE BASED ON WHAT WAS READ IN THE FIRST FILE IN THE INPUT LICEL FOLDER
        data_template['date'] = f"{2000+int(file_list[0][1:3])}-{int(file_list[0][3:4], 16):02d}-{int(file_list[0][4:6]):02d}" 
        
        # FILL data_available AND data_stauts BASED ON THE SITE STATUS --------------------------------------------------------------------------------
        if data_template['station']['status'] == "operational":
            for file_name in file_list: # SET 'TRUE' IN data_available IF THERE IS A LICEL FILE ACQUIRED IN THAT HOUR
                data_available[ int(file_name[6:8]) ] = True
                data_status   [ int(file_name[6:8]) ] = "operational"
            # data_status = ["operational"  for i in range(24)]

        if data_template['station']['status'] == "planned":
            for file_name in file_list: # SET 'TRUE' IN data_available IF THERE IS A LICEL FILE ACQUIRED IN THAT HOUR
                data_available[ int(file_name[6:8]) ] = True
            data_status = ["preliminary"  for i in range(24)]

        if data_template['station']['status'] == "closed":
            data_available = ["false" for i in range(24)]
            data_status    = ["na"    for i in range(24)]
        # -----------------------------------------------------------------------------------------------------------------------------------------------

        # UPDATE THE FIELDS BASED ON WHAT WAS READ IN THE INPUT FOLDER (ARGUMENT NUMBER 2) AND THE STATUS OF THE STATION
        for d in range( len(data_template['data']) ):
            data_template['data'][d]['available'][:] = data_available
            data_template['data'][d]['status'][:]    = data_status

        # CREATE THE NAME OF THE OUTPUT JSON FILE -----------------------------------------------------------------------------------------------------------
        output_json_file = f"{sys.argv[3]}{os.path.basename(sys.argv[1])}"
        file_name_date = f"{2000+int(file_list[0][1:3])}{int(file_list[0][3:4], 16):02d}{int(file_list[0][4:6]):02d}"

        start_index = output_json_file.find("TEMPLATE")
        end_index   = output_json_file.find(".json")
        if start_index == -1 or end_index == -1:
            print("Error in template filename. It must contain the string 'TEMPLATE'")
            exit(1)
        s = output_json_file[:start_index] + file_name_date + output_json_file[end_index:]
        output_json_file = s
        
        # WRITE THE OUTPUT JSON FILE -----------------------------------------------------------------------------------------------------------
        print(f"\nWriting to:", output_json_file)
        with open( output_json_file, "w") as file:
            json.dump(data_template, file, indent=4)

    else: # if ( os.path.isfile( sys.argv[1]) ) and ( os.path.isdir( sys.argv[2]) ):
        print("Wrong usage of the arguments: Usage:\n\t galion_auto_json_generator.json full_path_to_json_template_file full_path_to_LICEL_files_FOLDER full_path_to_output_json_file")

else: # if len(sys.argv) == 3:
    print( f"Wrong number of arguments. Usage:\n\t galion_auto_json_generator.json full_path_to_json_template_file full_path_to_LICEL_files_FOLDER full_path_to_output_json_file")


