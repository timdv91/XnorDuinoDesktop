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
#reqT = requestTest('http://0.0.0.0:8080')
#reqT = requestTest('http://192.168.5.45:8080')
#reqT = requestTest('http://192.168.1.51:8080')

# set the termination module temp offset and loop delay
# reqT.get('[16, 6, 2, 126, 10, 2, 145, 1]')
# reqT.get('[16, 5, 2, 126, 11, 1, 2]')

#reqT.get('[127, 5, 1, 126]', "WS")  # set the master for WriteSlave



while True:
    print("\n\nLoopstart")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")

    # Reading slave the easy method:
    # =====================================
    print("\n\nReading psu module easy")
    eCount = 0
    sCount = 0
    startTime = time.time()
    r = eval(reqT.get('[100, 0, 15]', "RS"))  # set de master for ReadSlave
    for i in range(len(r)):
        print(r[i], end=" ")
    print()
    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))

    # Reading slave the easy method:
    # =====================================
    print("\n\nReading psu module easy")
    eCount = 0
    sCount = 0
    startTime = time.time()
    r = eval(reqT.get('[101, 0, 15]', "RS"))  # set de master for ReadSlave
    for i in range(len(r)):
        print(r[i], end=" ")
    print()
    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))


    # Reading slave the easy method:
    # =====================================
    print("\n\nReading termination module easy")
    eCount = 0
    sCount = 0
    startTime = time.time()
    r = eval(reqT.get('[126, 0, 12]', "RS"))  # set de master for ReadSlave
    for i in range(len(r)):
        print(r[i], end=" ")
    print()
    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))


    # Reading slave the raw method:
    # ========================================================
    print("\n\nReading termination module raw")
    eCount = 0
    sCount = 0
    startTime = time.time()
    reqT.get('[16, 4, 1, 126, 0, 12]')   # set de master for read
    r = eval(reqT.get('[20, 12]'))       # read data received by the master
    for i in range(len(r)):
        print(r[i], end=" ")
    print()
    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))


    # Writing slave the easy method & raw method:
    # ========================================================
    print("\n\nWriting to slave modulles easy & raw: ")
    startTime = time.time()
    blinkSpeed = str(int(random.uniform(5, 50)))
    reqT.get('[124, 1, 2, 240, ' + blinkSpeed + ']', "WS")          # set the master for WriteSlave
    reqT.get('[16, 6, 2, 125, 1, 2, 240, ' + blinkSpeed + ']')
    print("--- %s seconds ---" % (time.time() - startTime))


    # Reading master the easy method (actually there is no difference to raw and easy)
    # ========================================================
    print("\n\nReading master the easy method using get: ")
    dataLib = []
    eCount = 0
    sCount = 0
    startTime = time.time()
    for i in range(0, 10):
        r = reqT.get('[0,15]', "RM")
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


    # Writing to master the easy method (protocol stays the same but there is protection against overwriting read only registers)
    # ========================================================
    print("\n\nWriting master the easy method using get: ")
    dataLib = []
    eCount = 0
    sCount = 0
    startTime = time.time()
    r = reqT.get('[14,1,' + blinkSpeed + ']', "WM") # 14 is an unused byte inside bus_memory on the slave
    print(eval(r))
    print("Errors: ", eCount, end=" | ")
    print("Success: ", sCount)
    print("--- %s seconds ---" % (time.time() - startTime))


    # Reading master the easy method (actually there is no difference to raw and easy)
    # ========================================================
    print("\n\nReading master the easy method using post: ")
    dataLib = []
    eCount = 0
    sCount = 0
    startTime = time.time()
    for i in range(0, 10):
        r = reqT.post('[0,15]', "RM")
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