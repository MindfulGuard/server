#!/bin/bash

if [ $# -ne 5 ];
then
echo "missing parameters <HOSTNAME> <ROOT_ACCESS_KEY> <ROOT_SECRET_KEY> <USER_ACCESS_KEY> <USER_SECRET_KEY>"
exit 1

elif ! command -v mc &> /dev/null
then
    curl -sSL https://dl.min.io/client/mc/release/linux-amd64/mc \
    --create-dirs \
    -o $HOME/minio-binaries/mc

    chmod +x $HOME/minio-binaries/mc
    export PATH=$PATH:$HOME/minio-binaries/
fi


hostname = "$1"
root_access_key = "$2"
root_secret_key = "$3"
user_access_key = "$4"
user_secret_key = "$5"

mc alias set minioadmin $hostname $root_access_key $root_secret_key

mc admin user add minioadmin $user_access_key $user_secret_key
mc admin policy attach ALIAS readwrite --user=$user_access_key