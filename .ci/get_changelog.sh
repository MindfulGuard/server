#!/bin/bash

# The script gets the latest version from the changelog.txt file

# Example of the contents of changelog.txt file:
# v0.0.2
#
# - New feature 1 in version 0.0.2
# - New feature 2 in version 0.0.2
#
# v0.0.1
#
# - New feature 1 in version 0.0.1
# - New feature 2 in version 0.0.1
#

# Output:
# v0.0.2
# - New feature 1 in version 0.0.2
# - New feature 2 in version 0.0.2

if [ $# -ne 1 ]; then
    echo "Usage: $0 <PATH_TO_FILE>"
    exit 1
fi

file_path=$1

if [ ! -f "$file_path" ]; then
    echo "File not found: $file_path"
    exit 1
fi

current_version=""
changes=""
last_version=""

while IFS= read -r line; do
    if [[ "$line" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        if [ -n "$current_version" ]; then
            if [ -z "$last_version" ]; then
                echo "$current_version"
                echo -e "$changes"
                exit 0
            fi
        fi
        last_version="$current_version"
        current_version="$line"
        changes=""
    elif [ -n "$current_version" ] && [ -n "$line" ]; then
        if [ -n "$changes" ]; then
            changes+=$'\n'
        fi
        changes+="$line"
    fi
done < "$file_path"