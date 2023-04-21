# GALION_Lidar_Tools
Set of tools for GALION Network (https://galion.world/) for metadata automation and submission.


## Introduction

The World Meteorological Organization (WMO) Global Atmospheric Watch (GAW) Aerosol Lidar Observation Network (GALION) was formed in 2008. GALION is a lidar network of networks organized through the GAW program to coordinate network activities and provide comprehensive profiling of atmospheric aerosols, clouds, gases, and thermodynamic structure (from https://galion.world/).


To homogenize the data, GALION Network uses JSON data files to report their measurements. This file contains metadata reporting general information about the site, its instrumentation and operational status, persons in charge, and the atmospheric variables output for the site. For these outputs, boolean-hourly data is filled up in the JSON files reporting if there is data available or not. Also, the hourly status of the measurement must be reported as: ***preliminary***, ***operational*** or **na**.

Since filling daily JSON files with hourly data is a time-consuming task to accomplish every day, this script was developed to solve this work automatically. Using tree input parameters: a JSON template, the path to the acquired lidar data and the output path to save the JSON files, this script can perform
* Creates a new JSON based on the template JSON file passed as the first argument.
* Fills the fields related to the data availability for each hour of the day. Also, set the right date inside the new JSON file.
* Save the output JSON file in the path passed as the third argument.

The script ***galion_auto_json_generator.py*** is a command line tool to fill the variable ***available*** inside the *json* file based on the saved LICEL lidar files.

## Installation
This Python code only needs three libraries to run: ***os***, ***sys*** and ***json***. All can be installed in a single command line using *pip*:

```
pip install os sys json
```

Once this is done, you are ready to run ***galion_auto_json_generator.py***.

## How to Use

The script ***galion_auto_json_generator.py*** is a command line tool 

### First Argument: Template file

### Second Argument: Licel data file types folder

### Third Argument: Output JSON file type folder

