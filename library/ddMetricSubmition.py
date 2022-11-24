import logging, json, time
from library.datadogApi import datadogApi
from library.generalFuncs import *

class StopParentLoop(Exception): pass

class ddMetricSubmition:
    def __init__(self):
        with open("./conf/config.json") as confJ:
            self.config = json.load(confJ)
        with open("./conf/mappings.json") as mapJ:
            self.mappings = json.load(mapJ)
        self.apis = self.config["apis"]
        self.baseMetricsRelation = self.mappings["metrics"]["baseMetricsRelation"]
        self.ddApi = datadogApi()
        self.__metricSubmitList = [{"series": []}]
        self.metricSubmitTemplate = '{"series": []}'
        self.metricJsonTemplate = '{"metric": "nameSample", "type": 3, "unit": "megabyte", "tags": [], "points": [{"timestamp": 0,"value": 0}]}'

    def getmetricSubmitList(self):
        return self.__metricSubmitList
    
    def addMetricToSubmit(self, name, timestamp, value, tags=None):
        metricToAdd = json.loads(self.metricJsonTemplate)
        metricToAdd['metric'] = str(name)
        metricToAdd['type'] = int(self.mappings["metrics"]['metrictypeid'])
        metricToAdd['unit'] = str(self.mappings["metrics"]['metricunit'])
        metricToAdd['points'][0]['timestamp'] = timestamp
        metricToAdd['points'][0]['value'] = value
        if tags is not None:
            metricToAdd['tags'] = tags
        
        lastMetricSubmitItem = self.__metricSubmitList[-1]
        for metricsJsonItem in self.__metricSubmitList:
            if jsonBytesSize(metricsJsonItem.copy())+52 > 512:
                if metricsJsonItem == lastMetricSubmitItem:
                    self.__metricSubmitList.append(json.loads(self.metricSubmitTemplate))
            else:
                metricsJsonItem["series"].append(metricToAdd)
    
    def convertBaseMetricsToFinalAndAddToSubmit(self, baseMetricsJson):
        timestamp = int(time.time())
        for metricName in baseMetricsJson:
            currentMetricJson = baseMetricsJson[metricName]
            baseMetricName = currentMetricJson['baseMetricName']
            tagToBeMetric = self.baseMetricsRelation[baseMetricName]['tagtobemetric']
            if len(currentMetricJson['series']) == 0:
                logging.error("Series array is empty for metric:", metricName, "| Skipping metric")
                continue
            for dataPoint in currentMetricJson['series']:
                if 'tag_set' not in dataPoint:
                    logging.error("tag_set not found in current dataPoint, check json content and double check mappings:\n", dataPoint)
                    continue
                tagSet = dataPoint['tag_set']
                metricValue = 0
                tagsToAdd = []
                try:
                    for tag in tagSet:
                        if tagToBeMetric in tag:
                            try:
                                metricValue = int(tag.split(":")[1])
                                continue
                            except Exception as e:
                                logging.error("Could not split or convert metric value, split result:", tag.split(":"), "| Current dataPoint:\n", dataPoint, "\n| Exception:\n", e)
                                raise StopParentLoop()
                        tagsToAdd.append(tag)
                except StopParentLoop:
                    continue
                self.addMetricToSubmit(metricName, timestamp, metricValue, tagsToAdd)

    def submitMetrics(self):
        responseList = []
        for item in self.getmetricSubmitList():
            logging.debug("Submit item:\n"+str(item))
            if len(item["series"]) == 0:
                responseList.append("No items in list to submit, not requesting API")
                return responseList
            responseList.append(self.ddApi.requestApi(self.apis["submitmetricapiurl"], 'post', json=item).text)
        return responseList
    
    def flushMetricsToSubmit(self):
        self.__metricSubmitList = []
        self.__metricSubmitList.append(json.loads(self.metricSubmitTemplate))