# GALION_Lidar_Tools
Set of tools for GALION Network (https://galion.world/) for metadata automation and submission.

<span style="color:red"> TO USE THIS SCRIPT, SOME KNOWLEDGE ABOUT GALION JSON FILES DATA TYPE IS RECOMMENDED. MORE INFORMATION ABOUT THIS CAN BE FOUND AT https://galion.world</span>

## Introduction

The World Meteorological Organization (WMO) Global Atmospheric Watch (GAW) Aerosol Lidar Observation Network (GALION) was formed in 2008. GALION is a lidar network of networks organized through the GAW program to coordinate network activities and provide comprehensive profiling of atmospheric aerosols, clouds, gases, and thermodynamic structures (from https://galion.world/).


To homogenize the data, GALION Network uses JSON data files to report their measurements. This file contains metadata reporting general information about the site, its instrumentation and operational status, persons in charge, and the atmospheric variables output for the site.

For these outputs, boolean-hourly data is filled up in the JSON files reporting if there is data available or not. Also, the hourly status of the measurement must be reported as: ***preliminary***, ***operational*** or **na**.

Since filling daily JSON files with hourly data is a time-consuming task to accomplish every day, this script was developed to solve this work automatically. Using tree input parameters: a JSON template, the path to the acquired lidar data and the output path to save the JSON files, this script can perform
* Creates a new JSON based on the template JSON file passed as the first argument.
* Fills the fields related to the data availability for each hour of the day. Also, set the right date inside the new JSON file.
* Save the output JSON file in the path passed as the third argument.

The automatic run of this script has to be performed using another script, running this code and passing the arguments correctly. Ie, it can be done with a Linux script or Python executed through a cronjob (in case of using Linux OS).


## Installation
This Python code only needs three libraries to run: ***os***, ***sys*** and ***json***. All can be installed in a single command line using *pip*:

```
pip install os sys json
```

Once this is done, you are ready to run ***galion_auto_json_generator.py***. Have in mind that the lidar files have to be run on the same PC where the lidar files are stored.

## How to Use

The script ***galion_auto_json_generator.py*** is a command line tool devoted to filling the variable ***available*** inside the ***JSON*** file. It also fills the ***date*** field.

The script has to be launched as:

```
python3 galion_auto_json_generator.py GALION_NET_SITENAME_TEMPLATE.json folder_path_to_lidar_files path_to_output_folder

```

Each of these arguments is explained in the following sub-sections.


### First Argument: Template file

Due to this script being devoted to filling the hourly-boolean variable ***available*** and ***date*** fields inside the JSON file, all the rest of the metadata has to be loaded from another source. This is accomplished using a JSON template file, passed as a first argument.

This template file is a regular GALION JSON file used for two main tasks:
* To create the output JSON filename.
* To load the general metadata fields related to the site status, contact persons, etc.

The JSON filename has to follow certain rules, and there are:

`GALION_NET_SITENAME_TEMPLATE.json`

Where:
- `GALION`: All JSON filenames for the GALION network must start with the word *GALION*.
- `NET`: Is the network name as is named inside the GALION Network (ie: *LALINET*).
- `SITENAME`: Is the name of the site as is named inside the GALION Network (ie: *OZONECEILAP*).
- `TEMPLATE`: Key word.

And the output JSON filename automatically generated will be: `GALION_NET_SITENAME_YYYYMMDD.json`

where `YYYYMMDD` is:

- `YYYY`: Year of the measurement (4 digits)
- `MM`: Month of the measurement (two digits).
- `DD`: Day of the measurement (two digits).

This JSON template file must already contain general information data about the site status, contact persons, and variable output, which are going to be copied to the output file. If some of these data have to be changed, by just changing the template file it will be mirrored in the output file.


### Second Argument: Licel data file folder

The second argument of this Python script must be the folder where the lidar files are located. The folder must contain **only the lidar files**. Any other file type will produce a script malfunction.
Another important feature is that their filenames must follow the Licel filenames conventions (more info at https://licel.com/raw_data_format.html). The rules for the filename are as follows:

`xYYMDDhh.mmssuu`

Where: 

* `x`: Arbitrary letter, usually someway representative of the site (one character).
* `YY`: Year (two digits). This script interprets this number as the number of years after the year 2000.
* `M`: Month (one digit) **in hexadecimal base***.
* `DD`: Day (two digits).
* `hh`: Hours (two digits).
* `mm`: Minutes (two digits).
* `ss`: Seconds (two digits).
* `uu`: miliseconds (two digits).

By reading the filename of the acquired files, we can know if there is data available at a certain hour (`available` variable of the JSON file). The status of this data has to be defined by the lidar operator, filling the state in the `status` variable of the template file passed as the first argument. This could be: `operational`, `preliminary` or `na`.


### Third Argument: Output JSON file folder

Path of the folder where the JSON files will be stored.

