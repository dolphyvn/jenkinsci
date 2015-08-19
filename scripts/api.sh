#!/bin/sh
SCRIPT_NAME=$1
CMD_MESS=$2
USERNAME='usersms'
PASSWORD='Ncajsd43jc'
KEY='MmckascKK322Ica'
checksum=`echo -n "$USERNAME$PASSWORD$SCRIPT_NAME$CMD_MESS$KEY" | md5sum`
SMS_MESS_ENCODE=`echo "$CMD_MESS" | sed 's/ /%20/g'`
echo $SMS_MESS_ENCODE
echo 'curl "http://sandbox.cronapi.123pay.vn/index.php?username=$USERNAME&password=$PASSWORD&scriptname=$SCRIPT_NAME&message=$SMS_MESS_ENCODE&checksum=$checksum"'
curl "http://sandbox.cronapi.123pay.vn/index.php?username=$USERNAME&password=$PASSWORD&scriptname=$SCRIPT_NAME&message=$SMS_MESS_ENCODE&checksum=$checksum"
