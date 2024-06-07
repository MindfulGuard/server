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

# Output (v0.0.2):
# - New feature 1 in version 0.0.2
# - New feature 2 in version 0.0.2

if [ $# -ne 2 ]; then
    echo "Usage: $0 <PATH_TO_FILE> <VERSION>"
    exit 1
fi

file_path=$1
version=$2

if [ ! -f "$file_path" ]; then
    echo "File not found: $file_path"
    exit 1
fi

current_version=""

while IFS= read -r line; do
    if [[ "$line" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        current_version="$line"
    elif [ "$current_version" = "$version" ] && [ -n "$line" ]; then
        echo "$line"
    fi
done < "$file_path"