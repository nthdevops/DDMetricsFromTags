from datetime import datetime, timedelta
import json

def previousMonth(dt):
   return dt.replace(day=1) - timedelta(days=1)

def jsonBytesSize(jsonDict):
   json_string = json.dumps(jsonDict)
   byteZon = json_string.encode("utf-8")
   return int(len(byteZon)/1000)

def metricConversion(conversionConfig, value):
   match conversionConfig['mode']:
        case 'div':
            return value/conversionConfig['by']
        case 'mult':
            return value*conversionConfig['by']
        case 'add':
            return value+conversionConfig['by']
        case 'sub':
            return value-conversionConfig['by']
        case _:
            return value   # case if is not found