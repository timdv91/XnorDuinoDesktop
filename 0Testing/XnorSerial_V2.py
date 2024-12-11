import requests
import time
import random

class requestTest():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        r = requests.get(str(self.URL + "/" + pPath), data=(pData))
        return r.text

    def post(self, pData, pPath=""):
        # POST request:
        r = requests.post(str(self.URL + "/" + pPath), data=(pData))
        return r.text

reqT = requestTest('http://127.0.0.1:8080')

#r = reqT.get('[5,1,0]', "WM") # 14 is an unused byte inside bus_memory on the slave

while True:

    r = eval(reqT.get('[5, 5]', "RM"))
    buf = []
    for i in range(0, len(r)):
        buf.append(r[i])
    print(buf)

    r = eval(reqT.get('[10, 4]', "RM"))
    buf = []
    for i in range(0, len(r)):
        buf.append(r[i])
    print(buf)

    for i in range(1, 127, 10):
        r = reqT.get('[16,3,3,' + str(i) + ',' + str(i+10) + ']', "WM")

        r = eval(reqT.get('[20, 10]', "RM"))
        buf = []
        for i in range(0, len(r)):
            buf.append(r[i])
        print(buf)

