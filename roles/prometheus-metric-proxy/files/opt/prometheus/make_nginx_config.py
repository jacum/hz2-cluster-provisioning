#!/usr/bin/python

# Produces haproxy config based on Marathon /v2/apps/?embed=apps.tasks
# 1 ports of tasks marked with a label 'prometheusPath' will be exported as /metrics/<task>/<instance>
# 2 the whole set of available URLs to scrap will be exported under /metrics

# prerequisites

import json
import urllib2
import commands
import argparse


def find_metric_port(mappings):
    port_position = 0

    for port in mappings:
        port_labels = port['labels']
        if 'prometheusPath' in port['labels']:
            return port_position, port_labels['prometheusPath'].strip('/')
        port_position += 1

    return -1, ''


parser = argparse.ArgumentParser()

parser.add_argument('-H', '--host', help='Marathon host', required=True)
parser.add_argument('-U', '--user',
                    help='User name to authenticate against Marathon',
                    default=None)
parser.add_argument('-P', '--password',
                    help='Password to authenticate against Marathon',
                    default=None, dest='password')

args = parser.parse_args()

marathon_url = "{host}/v2/apps/?embed=apps.tasks".format(host=args.host)
req = urllib2.Request(url=marathon_url,
                      headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, marathon_url, args.user, args.password)
auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)

opener = urllib2.build_opener(auth_manager)
urllib2.install_opener(opener)

apps_tasks_data = urllib2.urlopen(marathon_url).read()
raw_json = json.loads(apps_tasks_data)

this_host = commands.getoutput('cat /etc/default/mesos-slave | grep MESOS_HOSTNAME | sed -e "s/MESOS_HOSTNAME=//"')

proxy_config = ""
proxy_contents = ""

for app in raw_json['apps']:
    app_id = app['id'].strip('/')
    container = app['container']
    port_mappings = container['portMappings']

    (metric_port_position, metric_path) = find_metric_port(port_mappings)
    if metric_port_position >= 0:
        task_number = 0
        for task in app['tasks']:
            host = task['host']
            task_number = + 1
            if host == this_host:
                port = task['ports'][metric_port_position]
                proxy_contents += "/metrics/{app_id}/{task_number}\\n".format(app_id=app_id,
                                                                              task_number=task_number)
                proxy_config += """location = /metrics/{app_id}/{task_number} {{
    proxy_buffering off;
    proxy_pass http://{this_host}:{port}/{metric_path};
}}""".format(app_id=app_id,
             this_host=this_host,
             port=port,
             metric_path=metric_path,
             task_number=task_number)

print("""location = /metrics {{
    return 200 '{contents}';
    add_header Content-Type text/plain;
}}
{proxy_config}
""".format(contents=proxy_contents, proxy_config=proxy_config))
