
# clear ; python3 get_lidar_measurement_data.py ../licel_files/

import sys
import os

# LICEL FILE: a1542515.042996

# MAIN
if len(sys.argv) > 1:
   if os.path.isdir( sys.argv[1] ):
      hours_with_Data = [False for i in range(24)]
      print(f"BEFORE: hours_with_Data: {hours_with_Data}")

      file_list = os.listdir(sys.argv[1])

      for file_name in file_list:
         hours_with_Data[ int(file_name[6:8]) ] = True
      
      print(f"AFTER: hours_with_Data: {hours_with_Data}")

   else:
      print("Please specify a folder to list the files")
else:
   print("The scipt get_lidar_measurement_data need a directory passed as argument")


