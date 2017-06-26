#!/usr/bin/python
import sys
import requests
import json
import os
import datadog

options = {
    'api_key':os.environ['datadog_api_key'],
    'app_key':os.environ['datadog_app_key']
}


datadog.initialize(**options)


host = sys.argv[1:][0]
url = "http://{}:3333".format(host)

html = requests.get(url).text
json_string = html.split('\n')[1].split('<br><br>')[0]
json = json.loads(json_string)
result = json['result']

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
            dd_metrics.append({'metric':"mining.{}".format(metric), 'points':int(list_value), 'tags':["card:{}".format(index), "node:miner"]})
    else:
       dd_metrics.append({'metric':"mining.{}".format(metric), 'points':int(value),'tags':["node:miner"]})

datadog.api.Metric.send(dd_metrics)
