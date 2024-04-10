#!/bin/bash

if [ $# -ne 5 ]; then
    echo "Missing parameters <ENV_FILE> <POSTGRES_HOST> <MINIO_HOSTNAME> <ADMIN_LOGIN> <ADMIN_PASSWORD>"
    exit 0
fi

ENV_FILE="$1"
_POSTGRES_HOST_="$2"
_MINIO_HOSTNAME_="$3"
ADMIN_LOGIN="$4"
ADMIN_PASSWORD="$5"

source "$ENV_FILE"

make -f build/Makefile init \
admin_login="$ADMIN_LOGIN" \
admin_password="$ADMIN_PASSWORD" \
database_host="$_POSTGRES_HOST_" \
database_port="$POSTGRES_PORT" \
database_user="$POSTGRES_USER" \
database_password="$POSTGRES_PASSWORD" \
minio_hostname="$_MINIO_HOSTNAME_" \
minio_root_access_key="$MINIO_ROOT_USER" \
minio_root_secret_key="$MINIO_ROOT_PASSWORD" \
minio_user_access_key="$MINIO_USER_ACCESS_KEY" \
minio_user_secret_key="$MINIO_USER_SECRET_KEY"
