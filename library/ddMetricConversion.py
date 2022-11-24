import logging, json, time
from library.datadogApi import datadogApi
import time

class ddMetricConversion:
    def __init__(self):
        with open("./conf/config.json") as confJ:
            self.config = json.load(confJ)
        with open("./conf/mappings.json") as mapJ:
            self.mappings = json.load(mapJ)
        self.apis = self.config["apis"]
        self.baseMetricsRelation = self.mappings["metrics"]["baseMetricsRelation"]
        self.ddApi = datadogApi()
    
    def getBaseMetricData(self, fromParameter, toParameter, queryParameter):
        baseMetricData = json.loads(self.ddApi.requestApi(self.apis["getmetricdata"], 'get', urlParameters=['from='+fromParameter,'to='+toParameter,'query='+queryParameter]).text)
        return baseMetricData
    
    def createQueryForMetric(self, metricName):
        #Sample query: rollout:metricName{*} by {tag1,tag2,tag3}
        metricJson = self.baseMetricsRelation[metricName]
        query = ""
        query += metricJson["rollout"]+":"+metricName+"{*} by {"
        for tag in metricJson["tags"]:
            query += tag
            if not tag == metricJson["tags"][-1]:
                query += ","
        query += "}"
        return query

    def getAllBaseMetricsData(self):
        currentTime = int(time.time())
        lastMinute = currentTime-500
        baseMetricsJson = {}
        for metric in self.baseMetricsRelation:
            metricJson = self.baseMetricsRelation[metric]
            try:
                query = self.createQueryForMetric(metric)
            except Exception as e:
                logging.error("Error creating query for metric", metric, "| Exception:\n", e)
                continue
            try:
                baseMetricsJson[metricJson['metricname']] = self.getBaseMetricData(str(lastMinute), str(currentTime), query)
                baseMetricsJson[metricJson['metricname']]['baseMetricName'] = metric
            except Exception as e:
                logging.error("Error requesting api for metric", metric, ", using query", query, "| Exception:\n", e)
        return baseMetricsJson