import requests, json

class datadogApi:

    def __init__(self):
        with open("./conf/config.json") as f:
            self.config = json.load(f)
        self.ddKeys = self.config["keys"]
    
    def requestApi(self, urlApi, method, urlParameters=[], payload=None, headers=None, json=None):
        if headers is None:
            headers = {}
            headers["DD-API-KEY"] = self.ddKeys["apikey"]
            headers["DD-APPLICATION-KEY"] = self.ddKeys["appkey"]

        if len(urlParameters) > 0:
            urlApi += '?'
            last_item = urlParameters[-1]
            for param in urlParameters:
                urlApi += param
                if param == last_item: #If it is the last item, breaks the for and wont add & at the end
                    break
                urlApi += '&'

        return requests.request(method=method, url=urlApi, data=payload, headers=headers, json=json)