import requests

class requestTest():
    def get(self, pData):
        # GET request:
        URL = 'http://0.0.0.0:8080'
        r = requests.get(URL, data=(pData))
        print(r.text)

    def post(self, pData):
        # POST request:
        URL = 'http://0.0.0.0:8080'
        r = requests.post(URL, data=(pData))
        print(r.text)

requestTest().get('[6, 7, 2, 124, 0, 3, 0, 240, 50]')
requestTest().get('[0,6]')

requestTest().post('[6, 7, 2, 124, 0, 3, 0, 240, 50]')
requestTest().post('[0,6]')