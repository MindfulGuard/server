#!/bin/bash
mkdir -p /etc/nginx/certs

openssl req -x509 -nodes -newkey rsa:4096 -keyout /etc/nginx/certs/nginx.key \
-out /etc/nginx/certs/nginx.crt -days 365 -subj "/C=US"