#!/bin/sh

existing_config=/etc/nginx/default.d/metrics.conf
new_config=/tmp/metrics.conf

update_and_restart()
{
cp $new_config $existing_config
/sbin/service nginx restart
echo "config updated and reloaded"
}

/opt/prometheus/make_nginx_config.py -H http://cluster.jacum.com:8080 -U admin -P comeonletmein >$new_config
cmp --silent $existing_config $new_config || update_and_restart
