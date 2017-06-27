#!/usr/bin/python
import sys
import requests
import json
import yaml
import os
import datadog
import time


# Load config YAML
with open('config.yaml', 'r') as stream:
    config = yaml.load(stream)

# Check for required config values
for config_key in ['datadog_api_key', 'datadog_app_key']:
    if config_key in config:
        pass
    else:
        raise Exception("ERROR: {} missing from config.yaml!".format(config_key))

try:
    if len(config['miners']) > 0:
        pass
except:
    raise Exception("ERROR: No miners defined in config.yaml!")


options = {
    'api_key':config['datadog_api_key'],
    'app_key':config['datadog_app_key']
}
datadog.initialize(**options)


while True:
    for miner in config['miners']:

        host = miner['hostname']
        port = miner['port']

        url = "http://{}:{}".format(host, port)

        html = requests.get(url).text
        json_string = html.split('\n')[1].split('<br><br>')[0]
        json_object = json.loads(json_string)
        result = json_object['result']

        m = {}

        m['uptime'] = result[1]

        m['total_eth_rate'], m['eth_shares_accepted'], m['eth_shares_rejected'] = result[2].split(";")
        m['card_eth_rates'] = result[3].split(";")

        m['total_sia_rate'], m['sia_shares_accepted'], m['sia_shares_rejected'] = result[4].split(";")
        m['card_sia_rates'] = result[5].split(";")

        def even(number):
            if (number % 2 == 0):
                return True
            else:
                return False

        temp_fan_string = result[6].split(";")
        m['card_temperatures'] = []
        m['card_fan_speeds'] = []

        # The string alernates between temperature and fan speed for each card.
        # Temperatures are the even indexed values, fan speeds are the odd.
        for index, value in enumerate(temp_fan_string):
            if even(index):
                m['card_temperatures'].append(value)
            else:
                m['card_fan_speeds'].append(value)

        dd_metrics = []
        for metric, value in m.iteritems():
            if type(value) is list:
                for index, list_value in enumerate(value):
                    dd_metrics.append({'metric':"mining.{}".format(metric), 'points':int(list_value), 'tags':["card:{}".format(index), "node:{}".format(miner['hostname'])]})
            else:
               dd_metrics.append({'metric':"mining.{}".format(metric), 'points':int(value),'tags':["node:miner"]})

        try:
            datadog.api.Metric.send(dd_metrics)
            print "Sent metrics to Datadog:"
            print dd_metrics
            print "Sleeping 20 seconds..."
        except Exception:
            print "Error sending metrics to Datadog!"
        time.sleep(20)
