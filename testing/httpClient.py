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

# set the termination module temp offset and loop delay
# reqT.get('[16, 6, 2, 126, 10, 2, 145, 1]')
# reqT.get('[16, 5, 2, 126, 11, 1, 2]')

while True:

    print("\n")
    # directly read all values from the termination module:
    # ========================================================
    eCount = 0
    sCount = 0
    startTime = time.time()
    reqT.get('[16, 4, 1, 126, 0, 12]')   # set de master for read
    time.sleep(1)  # without a delay (such as reading the read command byte) overwrite at the start of the array seems to occur

    r = eval(reqT.get('[20, 12]'))       # read data received by the master
    for i in range(len(r)):
        print(r[i], end=" ")
    print()
    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))
    '''
    
    # set led blink on two mini controller boards:
    # ========================================================
    '''
    time.sleep(1)
    reqT.get('[16, 7, 2, 125, 0, 3, 0, 240, 5]')
    time.sleep(1)
    reqT.post('[16, 7, 2, 124, 0, 3, 0, 240, 5]')
    time.sleep(1)


    # speedtest get:
    # ========================================================
    print("\n\n GET speedtest: ")
    dataLib = []
    eCount = 0
    sCount = 0
    startTime = time.time()
    for i in range(0, 10):
        r = reqT.get('[0,14]')
        if (r != False):
            dataLib.append(eval(r))
            sCount += 1
        else:
            eCount += 1

    for o in range(0, len(dataLib)):
        print("[", end="")
        for i in range(0, len(dataLib[o])):
            print(dataLib[o][i], end=" ")
        print("]")

    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))
    time.sleep(1)

    # speedtest post:
    # ========================================================
    print("\n\n POST speedtest: ")
    dataLib = []
    eCount = 0
    sCount = 0
    startTime = time.time()
    for i in range(0, 10):
        r = reqT.post('[0,14]')
        if (r != False):
            dataLib.append(eval(r))
            sCount += 1
        else:
            eCount += 1

    for o in range(0, len(dataLib)):
        print("[", end="")
        for i in range(0, len(dataLib[o])):
            print(dataLib[o][i], end=", ")
        print("]")

    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))
    time.sleep(1)