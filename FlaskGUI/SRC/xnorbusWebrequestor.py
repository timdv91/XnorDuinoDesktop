import requests

class xnorbusWebrequestor():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        try:
            r = requests.get(str(self.URL + "/" + pPath), data=(pData))
            return r.text
        except requests.exceptions.ConnectionError:
            return None


    def post(self, pData, pPath=""):
        # POST request:
        try:
            r = requests.post(str(self.URL + "/" + pPath), data=(pData))
            return r.text
        except requests.exceptions.ConnectionError:
            return None
