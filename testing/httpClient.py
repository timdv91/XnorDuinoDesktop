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

#reqT.get('["00", "13", "A2", "00", "41", "92", "F3", "9E"]', "setRFmode") # set wireless master mode
reqT.get('["00", "00", "00", "00", "00", "00", "FF", "FF"]', "setRFmode") # set wireless master mode

reqT.get('[16, 9, 13, 00, 19, 162, 00, 64, 134, 78, 220]', "WM") # set wireless master mode

r = eval(reqT.get('[20, 9]'))  # read data received by the master
for i in range(len(r)):
    print(r[i], end=" ")
print()

#reqT.get('[16, 6, 14, 76, 79, 67, 65, 76]', 'WM')
#reqT.get('[16, 10, 14, 82, 69, 77, 79, 84, 69, 48, 48, 48]', 'WM') # set remote device name

quit()

#reqT.get('0', "clrRFmode")                 # read bus_memory from remote device
reqT.get('["00", "13", "A2", "00", "41", "92", "F3", "9E"]', "setRFmode") # set wireless master mode

quit()

reqT.get('0', "clrRFmode")                 # read bus_memory from remote device

#=======================================================================================================================
reqT.get('[9, 1, 41]', 'WM')
r = eval(reqT.get('[0, 14]', 'RM'))  # read data received by the master
for i in range(len(r)):
    print(r[i], end=" ")
print()

reqT.get('[126, 11, 1, 3]', "WS")          # set the master for WriteSlave
r = eval(reqT.get('[126, 0, 12]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

#=======================================================================================================================
reqT.get('[0, 19, 162, 00, 65, 146, 243, 158]', "setRFmode") # set wireless master mode
#=======================================================================================================================

reqT.get('[9, 1, 43]', 'WM')
r = eval(reqT.get('[0, 14]', "RM"))   # read bus_memory from remote device
for i in range(len(r)):
    print(r[i], end=" ")
print()

reqT.get('[126, 11, 1, 2]', "WS")          # set the master for WriteSlave
r = eval(reqT.get('[126, 0, 12]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

#=======================================================================================================================

quit()

print("\n\nReading remote master module raw")
eCount = 0
sCount = 0
startTime = time.time()


reqT.get('[16, 3, 12, 0, 14]')                 # read bus_memory from remote device
print("Requested data from remote device.")


r = eval(reqT.get('[20, 14]'))  # read data received by the master
for i in range(len(r)):
    print(r[i], end=" ")
print()
print("Errors: ", eCount, end=" | ")
print("Success: ", sCount)
print("--- %s seconds ---" % (time.time() - startTime))




print("Second test")




print("\n\nReading remote termination module raw")
eCount = 0
sCount = 0
startTime = time.time()
reqT.get('[16, 7, 11, 16, 4, 1, 126, 0, 12]')   # write action to remote device
print("send action to remote device.")


reqT.get('[16, 3, 12, 20, 12]')                 # read bus_memory from remote device
print("Requested data from remote device.")


r = eval(reqT.get('[20, 12]'))  # read data received by the master
for i in range(len(r)):
    print(r[i], end=" ")
print()
print("Errors: ", eCount, end=" | ")
print("Success: ", sCount)
print("--- %s seconds ---" % (time.time() - startTime))


quit()






#reqT.get('[127, 5, 1, 21]', "WS")

#reqT.get('[20, 7, 1, 10]', "WS")
#reqT.get('[21, 7, 1, 10]', "WS")
reqT.get('[20, 10, 1, 80]', "WS")
reqT.get('[21, 10, 1, 80]', "WS")
while(True):
    time.sleep(1)
    #reqT.get('[20, 10, 1, 255]', "WS")
    #reqT.get('[21, 10, 1, 255]', "WS")
    #reqT.get('[20, 8, 1, 45]', "WS")
    #reqT.get('[21, 8, 1, 45]', "WS")



    r = eval(reqT.get('[20, 6, 7]', "RS"))
    buf = []
    for i in range(0, len(r)):
        buf.append(r[i])
        print(r[i])
    print(buf)

    r = eval(reqT.get('[21, 6, 7]', "RS"))
    buf = []
    for i in range(0, len(r)):
        buf.append(r[i])
        print(r[i])
    print(buf)

quit()





reqT.get('[124, 1, 2, 0, 250]', "WS")          # set the master for WriteSlave


quit()
#reqT.get('[127, 5, 1, 123]', "WS")
r = eval(reqT.get('[123, 0, 10]', "RS"))
buf = []
for i in range(0, len(r)):
    buf.append(r[i])
    print(r[i])
print(buf)

quit()
# set the termination module temp offset and loop delay
# reqT.get('[16, 6, 2, 126, 10, 2, 145, 1]')
# reqT.get('[16, 5, 2, 126, 11, 1, 2]')

#r = reqT.get('[16, 2, 7, 1]', "WM")  # set the master for WriteSlave
#quit()
reqT.get('[16, 10, 5, 0, 124, 2, 5, 126, 9, 0, 15, 60]', "WM")  # set the master for WriteSlave
reqT.get('[16, 10, 5, 1, 124, 2, 20, 126, 9, 0, 15, 62]', "WM")  # set the master for WriteSlave
reqT.get('[16, 10, 5, 2, 125, 2, 5, 126, 9, 0, 15, 62]', "WM")  # set the master for WriteSlave
reqT.get('[16, 10, 5, 3, 125, 2, 20, 126, 9, 0, 15, 60]', "WM")  # set the master for WriteSlave

#reqT.get('[16, 13, 4, 0, 0, 1, 2, 3, 4, 5, 6, 62, 8, 9, 10]', "WM")  # set the master for WriteSlave

r = eval(reqT.get('[20, 3]', "RM"))
buf = []
for i in range(0, len(r)):
    buf.append(r[i])
print(buf)


'''
r = reqT.get('[16, 2, 7, 2]', "WM")  # set the master for WriteSlave
r = eval(reqT.get('[20, 1]', "RM"))
buf = []
for i in range(0, len(r)):
    buf.append(r[i])
print(buf)
'''

for i in range(0,92):
    print(i, " ", end=": ")
    r = reqT.get('[16, 2, 6, ' + str(i) + ']', "WM")  # set the master for WriteSlave
    r = eval(reqT.get('[20, 11]', "RM"))
    buf = []
    for o in range(0, len(r)):
        buf.append(r[o])
    print(buf)







quit()

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