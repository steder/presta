#!/usr/bin/env bash

<<EOF
This script generates a self signed x509 certificate
suitable for use with Twisted's SSL support.

You'll need to tweak the Common Name (CN)
below to match your servers FQDN so that clients
don't get the dreaded "this server doesn't appear to
be who you think it is" warnings.
EOF

set -e -u x

COMMON_NAME=presta.example.com
CERT_FILE=mycert.pem

openssl req -x509 -nodes -days 365 \
  -subj '/C=US/ST=Illinois/L=Chicago/CN=$HOSTNAME' \
  -newkey rsa:1024 -keyout $CERT_FILE -out $CERT_FILE
