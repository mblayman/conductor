#!/bin/sh
# This script renews all the Let's Encrypt certificates with a validity < 30 days

if ! /usr/bin/letsencrypt renew > /var/log/letsencrypt/renew.log 2>&1 ; then
    echo "Automated renewal failed:"
    cat /var/log/letsencrypt/renew.log
    exit 1
fi
/usr/sbin/service nginx restart
