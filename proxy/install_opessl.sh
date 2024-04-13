#!/bin/bash

if ! command -v openssl &> /dev/null; then
    CURRENT_PATH=$(pwd)

    cd /usr/local/src/

    curl https://www.openssl.org/source/openssl-1.1.1k.tar.gz \
    -O /usr/local/src/openssl-1.1.1k.tar.gz
    
    tar -xf openssl-1.1.1k.tar.gz

    cd openssl-1.1.1k

    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib

    make
    make install

    cd $CURRENT_PATH
fi