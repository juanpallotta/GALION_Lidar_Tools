#!/bin/bash
#
#	galion_curl.sh -f ./JSON_files/CEILAPOZONE/GALION_LALINET_CEILAPOZONE_20050806.json
#
#	WARNING NEW VERSION and NEW SCRIPT NAME (galion_curl):
#		you must now explicitly set uploaded file using a flag (galion_curl -f FILE.json)
#		older versions did not need a flag, just an arugment
#
# 	This script handles communication with the GALION server and its security controls
#		By default it uploads GALION metadata JSON files to the GALION server
#			It can also download any page or web result on the GALION server, including those requiring auth
#			Thus it can download GALION search results (the web page return, JSON or KML, etc)
#			For downloads: input URL (including any GET commands for forms)
#
#	This script handles authentication and CSRF tokens if required
#
#	This function accepts the following arguments:
#		-u		YOUR_USER:	your username for GALION website (optional, if not uses default) NOTE: USER only needed if desired GALION web page requires auth
#		-p		YOUR_PASS:	your password for GALION website (optional, if not uses default) NOTE: PASS only needed if desired GALION web page requires auth
#		-P		PROXY:		if your server uses a proxy server for outside connections, then set this to the proxy server URL (optional, if not set then uses default)
#		-U		URL:		the full URL to the GALION page you want to retrieve (optional, if not uses default which is the metadata upload API)
#		-f		FILE:  		full path to GALION Metadata JSON file to upload (optional, only required if uploading metadata files)
#
#	Notes on uploading files:
#		Upload only works with one file at a time
#		if upload is successful, the output from script will be "Pass"
#		if upload is unsuccessful, the output will be one of:
#			"Fail": this indicates that either login auth failed, or there was a CSRF token error. Use Debug feature for more info (see below)
#			"Fail" followed by additional lines of error reporting:	login auth and CSRF tokens are ok, but there were problems with the uploaded file. See error reporting.
#		In addition to satisfying authentication and CSRF, the user must have permissions to upload metadata files for your network
#			This is done with both the preset network usernames, but also others in the DCWG can be given permission from their user accounts (can use the online form version also)
#		If you decide to use your own upload method (e.g. python) please be aware that the GALION API utilizes both basic authentication and CSRF tokens.
#
#	Author:  Ellsworth J. Welton
#	Email:	ellsworth.j.welton@nasa.gov
#
#	History:
#		Created: 2022-12-15, EJ Welton
#		Updated: 2022-12-29, EJ Welton
#			fixed bug with extraction of CSRF token on Mac OS Bash, was leaving a space
#			added debug option
#		Updated: 2023-01-02, EJ Welton
#			added proxy
#		Updated: 2023-02-01, EJ Welton
#			changed script name to galion_curl
#			modified script to handle ANY communication with the GALION server, not just uploading metadata files
#			can now download any GALION web page/result even if requiring auth
#			this required a change to the inputs. If uploading a file you MUST now set it with a flag ( -f FILE.json)
#
#

### Set defaults if desired
DEFAULT_USER="LALINET"
DEFAULT_PASS="m*a7GgH!6ZZ2Mn50"
DEFAULT_PROXY=""
DEFAULT_URL=https://galion.world/api/galion_metadata_upload

### If uploads are failing with simple response "Fail", uncomment DEBUG variable below and make it equal to stdout
###		this will output the webserver response to both login and CSRF authentication attempts (only outputs information if either are failing)
### 	if login auth fails, check user and password
###		if CSRF verification failed:
###			please uncomment the echo $DJANGO_TOKEN and echo $DJANGO_TOKEN_VALUE lines in script below
###			run script again
###			copy output on screen and send to script author for more help
DEBUG_AUTH_AND_TOKEN="null"
#DEBUG_AUTH_AND_TOKEN="stdout"


while getopts f:u:p:P:U: flag
do
    case "${flag}" in
		f) FILE=${OPTARG};;
        u) YOUR_USER=${OPTARG};;
        p) YOUR_PASS=${OPTARG};;
        P) PROXY=${OPTARG};;
        U) URL=${OPTARG};;
    esac
done

if [ -z "$URL" ]
then
	URL=$DEFAULT_URL # set this to fixed default
fi

if [ -z "$FILE" ] && [[ "galion_metadata_upload" == *"$URL"* ]];
then
	echo "ERROR: must input a full path to file"
	exit 1
fi

if ! test -f "$FILE" && [[ "galion_metadata_upload" == *"$URL"* ]]; then
    echo "ERROR: file does not exist"
    exit 1
fi

if [ -z "$YOUR_USER"]
then
	YOUR_USER=$DEFAULT_USER # set this to fixed default
fi

if [ -z "$YOUR_PASS"]
then
	YOUR_PASS=$DEFAULT_PASS # set this to fixed default
fi

if [ -z "$PROXY"]
then
	PROXY=$DEFAULT_PROXY # set this to fixed default
fi
if [ "$PROXY" != "" ]
then
	PROXY="-x "$PROXY
fi


LOGIN_URL=https://galion.world/accounts/login/
COOKIES=cookies.txt

CURL_BIN="curl -s -c $COOKIES -b $COOKIES $PROXY -e $LOGIN_URL"
CHECK_CONNECTION=$($CURL_BIN $LOGIN_URL) 
if [ "$CHECK_CONNECTION" == "" ]
then
	echo "Fail: "$(basename -- $FILE)": initial connection to GALION server failed, might be a proxy problem"
	exit
fi

DJANGO_TOKEN="csrfmiddlewaretoken=$(grep csrftoken $COOKIES | sed 's/^.*csrftoken\s*[[:space:]]//g')"
### Uncomment line below and run if CSRF verification is failing
#echo $DJANGO_TOKEN

$CURL_BIN -d "$DJANGO_TOKEN&username=$YOUR_USER&password=$YOUR_PASS" -X POST $LOGIN_URL > /dev/$DEBUG_AUTH_AND_TOKEN

DJANGO_TOKEN="csrfmiddlewaretoken=$(grep csrftoken $COOKIES | sed 's/^.*csrftoken\s*[[:space:]]//g')"
### Uncomment line below and run if CSRF verification is failing
#echo $DJANGO_TOKEN

parts=(${DJANGO_TOKEN//\=/ })
DJANGO_TOKEN_VALUE=${parts[1]}
### Uncomment line below and run if CSRF verification is failing
#echo $DJANGO_TOKEN_VALUE

if [ -z "$FILE" ];
then
	$CURL_BIN -H "X-CSRFToken: $DJANGO_TOKEN_VALUE" -X GET $URL
else
	$CURL_BIN \
		-H "X-CSRFToken: $DJANGO_TOKEN_VALUE" \
		-H "Content-type: multipart/form-data" \
		-X POST -F "filename=@$FILE" -F "upload_type=curl" $URL
fi

rm $COOKIES
