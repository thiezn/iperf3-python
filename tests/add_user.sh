#!/bin/bash

# Command line positional parameters
USER=$1
PASSWD=$2
AUTHORIZED_USERS_FILE=$3

# Create the "authorized_users.txt" file
# Format is
# username,sha256hash("{username},password")
SHA256_USER_PASSWD=`echo -n {$USER}$PASSWD | openssl dgst -sha256 -binary | xxd -p -c 256`
echo "$USER,$SHA256_USER_PASSWD" >> $AUTHORIZED_USERS_FILE
