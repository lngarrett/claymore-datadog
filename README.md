# claymore-datadog
Docker container to send Claymore miner data to Datadog.

## Config
Copy `config.yaml.example` to `config.yaml` and edit it to suit your environment.

````yaml
datadog_api_key: YOURKEYHERE
datadog_app_key: YOURKEYHERE
miners:
  - hostname: 192.168.3.240
    port: 3333
````

All keys are required, and you must specify at least one miner.

## Installation
````bash
docker build -t claymonitor .
docker run --name="claymonitor" -d --restart="always" claymonitor
````
