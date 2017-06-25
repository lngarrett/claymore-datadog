# claymore-datadog
Script to send Claymore miner data to Datadog.

## Installation
````bash
pip install datadog --user
pip install requests --user
export datadog_api_key=YOURKEYHERE
export datadog_app_key=YOURKEYHERE
````

## Usage
`./claymonitor.py <miner_ip>`


## Cron
Run this in cron to send metrics every minute.

````bash
datadog_app_key=YOURKEYHERE
datadog_api_key=YOURKEYHERE
* * * * * /usr/bin/python /home/logan/code/claymore-datadog/claymonitor.py 192.168.3.240 > ~/claymonitor.log 2>&1
````
