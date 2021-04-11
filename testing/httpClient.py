import requests
import time

class requestTest():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData):
        # GET request:
        r = requests.get(self.URL, data=(pData))
        return r.text

    def post(self, pData):
        # POST request:
        r = requests.post(self.URL, data=(pData))
        return r.text



#reqT = requestTest('http://0.0.0.0:8080')
reqT = requestTest('http://192.168.5.45:8080')

reqT.get('[6, 7, 2, 125, 0, 3, 0, 240, 5]')
reqT.post('[6, 7, 2, 124, 0, 3, 0, 240, 5]')



# speedtest get:
print("\n GET speedtest: ")
dataLib = []
eCount = 0
sCount = 0
startTime = time.time()
for i in range(0, 10):
    r = reqT.get('[0,6]')
    if (r != False):
        dataLib.append(eval(r))
        sCount += 1
    else:
        eCount += 1

print(dataLib)
print(dataLib[0][4])
print("Errors: ", eCount, end=" | ")
print("Success: ", sCount)
print("--- %s seconds ---" % (time.time() - startTime))

# speedtest post:
print("\n POST speedtest: ")
dataLib = []
eCount = 0
sCount = 0
startTime = time.time()
for i in range(0, 10):
    r = reqT.post('[0,6]')
    if (r != False):
        dataLib.append(eval(r))
        sCount += 1
    else:
        eCount += 1

print(dataLib)
print(dataLib[0][4])
print("Errors: ", eCount, end=" | ")
print("Success: ", sCount)
print("--- %s seconds ---" % (time.time() - startTime))