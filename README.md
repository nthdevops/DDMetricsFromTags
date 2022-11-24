# Convert Tag Values into Metrics

## Configuration

### Basic config
Edit the name of the file config.json.template to config.json<br />
In the file edit:
```
    "keys": {
        "apikey": "",
        "appkey": ""
    }
```
Adding the api key and app key.

### Optional script config
If you want to change the frequency that the script submit metrics or/and the log level, change:
```
    "script": {
        "sleepsecs": 60,
        "loglevel": "WARN"
    }
```

### Mappings config
In mappings, edit the metrics unit, example:
```
"metricunit": "megabyte"
```
Also edit the json in the key "baseMetricsRelation", adding each metric you want to process, as the template indicates, example:
```
            "gcp.cloudfunctions.function.user_memory_bytes.avg":{
                "rollout": "avg",
                "tags": ["function_name", "memory", "project_id"],
                "tagtobemetric": "memory",
                "metricname": "gcp.cloudfunctions.function.user_memory_bytes.total"
            }
```
Is this example, the tag memory is going to be the value in the metric's datapoints, and the other tags will be added to this new metric

## Doubts?
> Send an email to [Nathan Pereira](mailto:nathan.pereira@delfia.tech)