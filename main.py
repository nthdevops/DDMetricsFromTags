import logging, time, json
from library.generalFuncs import *
from library.ddMetricConversion import ddMetricConversion
from library.ddMetricSubmition import *

with open("./conf/config.json") as f:
    config = json.load(f)
scriptConfig = config["script"]

logging.basicConfig(filename="./script.log", level=getattr(logging, scriptConfig["loglevel"]), format='%(asctime)s %(levelname)s %(message)s')
ddMetricConv = ddMetricConversion()
ddMetricSub = ddMetricSubmition()
sleepSecs = scriptConfig["sleepsecs"]

logging.info("\nScript start")

while 1:
    logging.info("Running routine")

    ddMetricSub.flushMetricsToSubmit()
    baseMetricsJson = ddMetricConv.getAllBaseMetricsData()
    if baseMetricsJson == {}:
        logging.error("baseMetricsJson is empty, check config and mappings, exiting")
        exit()
    ddMetricSub.convertBaseMetricsToFinalAndAddToSubmit(baseMetricsJson)
    logging.debug("SubmitList:\n"+str(ddMetricSub.getmetricSubmitList()))
    submitReturns = ddMetricSub.submitMetrics()
    for item in submitReturns:
        logging.info("Api response: "+str(item))
    logging.info("Routine ended, sleepSecs: "+str(sleepSecs))
    time.sleep(sleepSecs)