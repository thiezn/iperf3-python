#!/bin/bash

# Generate the private key, public key, and authorized users files we need
# to be able to run a test.

# This presumes you have openssl available.
# Also note this slightly deviates from the iperf3 man page as of August 2020 when
# they suggest using sha256sum. This isn't by default available on MacOS
# So I just use openssl for it, too.

# You can test this works by running the following commands.
#
# server:
#   iperf3 -s -p 2310 --authorized-users-path authorized_users.txt --rsa-private-key-path private_not_protected.pem
#
# client:
#   IPERF3_PASSWORD=test iperf3 -c 127.0.0.1 -p 2310 --username=test --rsa-public-key-path public.pem
#
# This should output a normal test run.

# Generate the server side unecrypted private key that the server will use.
openssl genrsa -out private_not_protected.pem 2048

# Generate the public key that the client will use send stuff privately to the server.
openssl rsa -in private_not_protected.pem -outform PEM -pubout -out public.pem

# Create the "authorized_users.txt" file
# Format is
# username,sha256hash("{username},password")
AUTHORIZED_USERS_FILE="authorized_users.txt"

# Create user with test, test username, password.
rm $AUTHORIZED_USERS_FILE
./add_user.sh test test $AUTHORIZED_USERS_FILE

