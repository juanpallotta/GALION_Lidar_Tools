#!/bin/bash

# clean ; ./bulk_galion_auto_json_generator.sh GALION_LALINET_CEILAPOZONE_TEMPLATE_OPERATIONAL.json /mnt/Disk-1_8TB/Argentina/test/ ./JSON_OUT/

clear

echo ""
echo ""

# MAIN FOLDER CONTAINING ALL THE FOLDERS WITH THE LIDAR DATA 
    if [ $# -eq 3 ]
    then # RIGHT NUMBER OF ARGUMENTS

        if [ -f $1 ] && [ -d $2 ] && [ -d $3 ]
        then
            echo -e "\n\t\t\t* RIGHT ARGUMENTS TYPE *\n"

            PATH_IN_LIST=$(ls -d -1 $2*/)
            for p in $PATH_IN_LIST
            do
                python3 galion_auto_json_generator.py $1 $p $3
            done

            # IF YOU NEED TO UPLOAD JSON FILES, UNCOMENT THE NEXT 6 LINES
            # echo -e "\n\nUploading the JSON files generated...\n"
            # JSON_FILES=$(ls $3*)
            # for f in $JSON_FILES
            # do
            #     echo -e "Uploading: "$f
            #     ./galion_curl.sh -f $f
            #     echo -e "\n"
            # done

        else
            echo -e "\n\t\t\t* WRONG ARGUMENTS TYPES *\n"
        fi

    else # THE SCRIPT HAVE ONE A ARGUMENT
        echo -e "\n\t\t\t* WRONG NUMBER OF ARGUMENTS *\n"
    fi

echo ""
echo "GALION' LIDAR SCRIPT ENDED."
echo ""

exit 0
