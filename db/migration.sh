#!/bin/bash

if [ $# -ne 7 ]; then
    echo "Missing parameters <PATH_TO_MIGRATIONS> <UP_OR_DROP> <POSTGRES_USER> <POSTGRES_PASSWORD> <POSTGRES_HOST> <POSTGRES_PORT> <POSTGRES_DB>"
    exit 1
fi

PATH_TO_MIGRATIONS="$1"
MIGRATION_TYPE="$2"
PGSQL_USER="$3"
PGSQL_PASSWORD="$4"
PGSQL_HOST="$5"
PGSQL_PORT="$6"
PGSQL_DB="$7"
PGSQL_STRING="postgresql://$PGSQL_USER:$PGSQL_PASSWORD@$PGSQL_HOST:$PGSQL_PORT/$PGSQL_DB?sslmode=disable"

MAX_RETRIES=5
RETRY_INTERVAL=60

retry_count=0

while [ $retry_count -lt $MAX_RETRIES ]; do
    if [ "$MIGRATION_TYPE" == "up" ]; then
        if migrate -database "$PGSQL_STRING" -path "$PATH_TO_MIGRATIONS" up; then
            break
        else
            echo "Migration failed. Retrying in $RETRY_INTERVAL seconds..."
            sleep $RETRY_INTERVAL
        fi
    elif [ "$MIGRATION_TYPE" == "down" ]; then
        if migrate -database "$PGSQL_STRING" -path "$PATH_TO_MIGRATIONS" down; then
            break
        else
            echo "Migration failed. Retrying in $RETRY_INTERVAL seconds..."
            sleep $RETRY_INTERVAL
        fi
    else
        echo "Invalid migration type. Use 'up' or 'down'."
        exit 1
    fi
    
    ((retry_count++))
done

if [ $retry_count -eq $MAX_RETRIES ]; then
    echo "Maximum number of retries reached. Migration failed."
    exit 1
fi