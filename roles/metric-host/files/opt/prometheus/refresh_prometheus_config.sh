#!/bin/sh

existing_config=/etc/prometheus/marathon-tasks.json
new_config=/tmp/prometheus.yml

update_and_restart()
{
cp $new_config $existing_config
/sbin/service prometheus reload
echo "config updated and reloaded"
}

/opt/prometheus/make_prometheus_config.py >$new_config
cmp --silent $existing_config $new_config || update_and_restart
