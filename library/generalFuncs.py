from datetime import datetime, timedelta
import json

def previousMonth(dt):
   return dt.replace(day=1) - timedelta(days=1)

def jsonBytesSize(jsonDict):
   json_string = json.dumps(jsonDict)
   byteZon = json_string.encode("utf-8")
   return int(len(byteZon)/1000)

def metricConversion(conversionConfig, value):
    matchOn = conversionConfig['mode']
    if matchOn == 'div':
        return value/conversionConfig['by']
    elif matchOn == 'mult':
        return value*conversionConfig['by']
    elif matchOn == 'add':
        return value+conversionConfig['by']
    elif matchOn == 'sub':
        return value-conversionConfig['by']
    else:
        return value   # case if is not found