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

[u'9.5 - ETH', u'1749', u'159767;3308;0', u'26687;26768;26004;26412;26783;27110', u'3727894;2688;0', u'622706;624594;606782;616281;624945;632586', u'73;75;71;75;72;75;74;75;78;75;67;75', u'eth-us-east1.nanopool.org:9999;sia-us-east1.nanopool.org:7777', u'0;0;0;0']

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
