from datetime import datetime, timedelta
import json

def previousMonth(dt):
   return dt.replace(day=1) - timedelta(days=1)

def jsonBytesSize(jsonDict):
   json_string = json.dumps(jsonDict)
   byteZon = json_string.encode("utf-8")
   return int(len(byteZon)/1000)