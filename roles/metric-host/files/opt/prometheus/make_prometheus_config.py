#!/usr/bin/python

# Produces haproxy config based on Marathon /v2/apps/?embed=apps.tasks
# 1 ports of tasks marked with a label 'prometheusPath' will be exported as /metrics/<task>/<instance>
# 2 the whole set of available URLs to scrap will be exported under /metrics

# prerequisites

import json
import urllib2

# configuration of marathon cluster
metric_proxy_port = 8008  # marathon metric proxy
metric_host_port = 9100  # marathon host exporter

scheme = 'http://'

metric_proxy_hosts = [
    {"name": 'hz2-n01', "host": '192.168.122.101'},
    {"name": 'hz2-n02', "host": '192.168.122.102'},
    {"name": 'hz2-n03', "host": '192.168.122.103'},
    {"name": 'hz2-n04', "host": '192.168.122.104'},
    {"name": 'hz2-n05', "host": '192.168.122.105'},
    {"name": 'hz2-n06', "host": '192.168.122.106'},
    {"name": 'hz2-n07', "host": '192.168.122.107'},
    {"name": 'hz2-n08', "host": '192.168.122.108'}
]

######### for the case http basic auth is needed
#
# password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
# password_manager.add_password(None, marathon_url, args.user, args.password)
# auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
#
# opener = urllib2.build_opener(auth_manager)
# urllib2.install_opener(opener)

marathon_tasks = ""


def fetchJobsFrom(host):
    try:
        return json.loads(urllib2.urlopen(scheme + host + ":" + str(metric_proxy_port) + "/metrics").read())
    except:
        #        print("Can't fetch services from " + host)
        return []


for metered_host in metric_proxy_hosts:
    host = metered_host['host']
    for job in fetchJobsFrom(host):
        marathon_tasks += """
  - job_name: '{name}'
    metrics_path: {url}
    static_configs:
    - targets: ['{host}:{port}']""".format(name=job['job'], host=host, port=metric_proxy_port, url=job['url'])

print(marathon_tasks)
