import requests
import time
import random
import struct

class convertIntToBytes:
    def __init__(self):
        None

    def conv(self, pIntVal):
        y1, y2, y3, y4 = (pIntVal & 0xFFFFFFFF).to_bytes(4, 'little')  # Use 'big' for big-endian; on 3.11+, you can omit it entirely, with 'big' being the default
        return y1, y2

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


# compressor pressure sensors with relay controls:

reqT = requestTest('http://192.168.1.64:8080')
#reqT = requestTest('http://127.0.0.1:8080')
#reqT = requestTest('http://0.0.0.0:8080')
#reqT = requestTest('http://192.168.5.45:8080')
#reqT = requestTest('http://192.168.1.51:8080')

'''
# Testing XbeeServer
reqT = requestTest('http://192.168.1.64:8081')
r = reqT.get('["0013A20041BD0FBA","set_io_configuration()","IOLine.DIO12", "IOMode.DIGITAL_OUT_LOW"]', "W")
print(r)
r = reqT.get('["0013A20041BD0FBA","get_io_configuration()","IOLine.DIO12"]', "R")
print(r)
r = reqT.get('["0013A20041BD0FBA","set_pwm_duty_cycle()","IOLine.DIO10_PWM0", "50"]', "W")
print(r)
r = reqT.get('["0013A20041BD0FBA","get_pwm_duty_cycle()","IOLine.DIO10_PWM0"]', "R")
print(r)
'''




quit()

# Configure stepper driver:
reqT.get('[127, 11, 2, 15, 64]', "WS")  # 10s 1s 30s 5s
time.sleep(1)

# set steps to take on stepper driver:
y1, y2 = convertIntToBytes().conv(1200)
reqT.get('[127, 13, 3, 120, ' + str(y2) + ', ' + str(y1) + ']', "WS")
#time.sleep(1)
#reqT.get('[127, 13, 1, 160]', "WS")  # 10s 1s 30s 5s
time.sleep(10)

# set steps to take on stepper driver:
y1, y2 = convertIntToBytes().conv(-1200)
reqT.get('[127, 13, 3, 120, ' + str(y2) + ', ' + str(y1) + ']', "WS")
#time.sleep(1)
#reqT.get('[127, 13, 1, 160]', "WS")  # 10s 1s 30s 5s
time.sleep(1)

# read registers from stepper driver:
r = eval(reqT.get('[127, 6, 10]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

vccADC = r[2]<<8 | r[3]
vcc = vccADC*(20/751)
print(vccADC)
print(vcc)

print()

stepsToHome = r[0]<<8 | r[1]
print(stepsToHome)






'''
/* Bus memory layout: 
 *   1 to 5 - Occupied by XnorBusMemoryMap
 *   6 - EMPTY
 *   7 - EMPTY
 *   8 - EMPTY
 *  10 - STEPS of stepper motor (divided by 4)
 *  11 - Hold timeout after standstill (0 = indef)
 *  12 - Hold current
 *  13 - SPEED
 *  14 - 15: float split in 4 bytes with degrees of rotation ??
 */
'''













quit()
y1, y2 = convertIntToBytes().conv(200)
reqT.get('[127, 11, 3, 90, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s
time.sleep(1)
y1, y2 = convertIntToBytes().conv(-200)
reqT.get('[127, 11, 3, 90, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s

time.sleep(1)

y1, y2 = convertIntToBytes().conv(50)
reqT.get('[127, 11, 3, 30, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s
time.sleep(1)
y1, y2 = convertIntToBytes().conv(-50)
reqT.get('[127, 11, 3, 30, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s

time.sleep(1)

y1, y2 = convertIntToBytes().conv(-25)
reqT.get('[127, 11, 3, 5, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s
time.sleep(3)
y1, y2 = convertIntToBytes().conv(25)
reqT.get('[127, 11, 3, 5, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s
time.sleep(3)

y1, y2 = convertIntToBytes().conv(400)
reqT.get('[127, 11, 3, 60, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s
time.sleep(3)
y1, y2 = convertIntToBytes().conv(-400)
reqT.get('[127, 11, 3, 255, ' + str(y2) + ', ' + str(y1) + ']', "WS")  # 10s 1s 30s 5s
time.sleep(1)

quit()
reqT.get('[127, 11, 2, 1, 200]', "WS")  # 10s 1s 30s 5s
r = eval(reqT.get('[127, 9, 4]', "RS"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()
time.sleep(1)


quit()
for i in range(0, 200):
    print(i)
    reqT.get('[127, 11, 2, 30, 1]', "WS")  # 10s 1s 30s 5s
    time.sleep(2)
quit()

while True:
    reqT.get('[127, 11, 2, 180, 200]', "WS") #10s 1s 30s 5s
    time.sleep(1)
    reqT.get('[127, 11, 2, 180, 100]', "WS") #10s 1s 30s 5s
    time.sleep(1)
    reqT.get('[127, 11, 2, 180, 10]', "WS")  # 10s 1s 30s 5s
    time.sleep(1)
    reqT.get('[127, 11, 2, 180, 190]', "WS")  # 10s 1s 30s 5s
    time.sleep(1)
    reqT.get('[127, 11, 2, 180, 200]', "WS") #10s 1s 30s 5s
    time.sleep(1)
    reqT.get('[127, 11, 2, 180, 100]', "WS") #10s 1s 30s 5s
    time.sleep(1)
    r = eval(reqT.get('[127, 10, 3]', "RS"))
    print("ID: ", end="")
    for i in range(len(r)):
        print(r[i], end=" ")
    print()

    time.sleep(5)
quit()


id1 = '50'
id2 = '60'
reqT.get('['+id1+', 12, 1, 64]', "WS")
reqT.get('['+id2+', 12, 1, 64]', "WS")
quit()


while True:
    reqT.get('['+id+', 12, 1, 32]', "WS")
    r = eval(reqT.get('['+id+', 12, 1]', "RSC"))
    print("ID: ", end="")
    for i in range(len(r)):
        print(r[i], end=" ")
    print()

    reqT.get('['+id+', 12, 1, 64]', "WS")
    r = eval(reqT.get('['+id+', 12, 1]', "RSC"))
    print("ID: ", end="")
    for i in range(len(r)):
        print(r[i], end=" ")
    print()


quit()


r = eval(reqT.get('[20, 10, 1]', "RSC"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

reqT.get('[20, 10, 1, 144]', "WS")

r = eval(reqT.get('[20, 10, 1]', "RSC"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

quit()



r = eval(reqT.get('[20, 0, 5]', "RSC"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()


r = eval(reqT.get('[126, 0, 5]', "RSC"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()


r = eval(reqT.get('[20, 0, 5]', "RSC"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()


r = eval(reqT.get('[126, 0, 5]', "RSC"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()





quit()

#reqT.get('[127, 5, 1, 69]', "WS")
#reqT.get('[69, 9, 2, 0, 125]', "WS")
reqT.get('[69, 11, 3, 1, 125, 125]', "WS")



quit()

reqT.get('[99, 6, 1, 50]', "WS")
reqT.get('[99, 15, 2, 2, 2]', "WS") # timed ctrl: (inverted) 3, (normal) 2

r = eval(reqT.get('[99, 15, 2]', "RS"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

reqT.get('[99, 25, 4, 1, 1, 3, 5]', "WS") #10s 1s 30s 5s
r = eval(reqT.get('[99, 25, 4]', "RS"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()


quit()

reqT.get('[99, 6, 1, 5]', "WS")                                   # set the master for WriteSlave
reqT.get('[99, 7, 10, 2, 52, 1, 75, 1, 7, 1, 2, 0, 0]', "WS")     # set the master for WriteSlave


r = eval(reqT.get('[99, 6, 11]', "RS"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()


r = eval(reqT.get('[99, 17, 8]', "RS"))
print("V: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

quit();




# COMATE board:
# =============================================

r = eval(reqT.get('[8, 0, 4]', "RS"))
print("ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

r = eval(reqT.get('[8, 4, 1]', "RS"))
print("FW ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

r = eval(reqT.get('[8, 5, 1]', "RS")) # I2C ID parameter is not set and not used
print("I2C ID: ", end="")
for i in range(len(r)):
    print(r[i], end=" ")
print()

print("========================================")
r = eval(reqT.get('[8, 6, 8]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

# solarvoltage voltage
value = r[0] << 8 | r[1]
print("solar voltage: " + str(value/1000) + "V")

# solar current
value = r[2] << 8 | r[3]
print("solar current: " + str(value/1000) + "A")

# watt / hour
value = r[4] << 8 | r[5]
print("watt hour: " + str(value) + "Wh")

# batt voltage
voltage = r[6] << 8 | r[7]
print("batt votlage: " + str(voltage/1000) + "V")


print("========================================")
r = eval(reqT.get('[8, 14, 8]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

# cell voltage 1
voltage = r[0] << 8 | r[1]
print("Cell voltage 0: " + str(voltage/1000) + "V")

# cell voltage 2
voltage = r[2] << 8 | r[3]
print("Cell voltage 1: " + str(voltage/1000) + "V")

# cell voltage 3
voltage = r[4] << 8 | r[5]
print("Cell voltage 2: " + str(voltage/1000) + "V")

# cell voltage 4
voltage = r[6] << 8 | r[7]
print("Cell voltage 3: " + str(voltage/1000) + "V")


print("========================================")
r = eval(reqT.get('[8, 22, 8]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

# humidity outside:
value = r[0] << 8 | r[1]
print("Humidity outside: \t\t" + str(value/100) + " %")

# temperature outside:
value = r[2] << 8 | r[3]
print("Temperature outside: \t" + str(value/100) + "°C")

# humidity tube:
value = r[4] << 8 | r[5]
print("Humidity tube: \t\t\t" + str(value/100) + " %")

# temperature tube:
value = r[6] << 8 | r[7]
print("Temperature tube: \t\t" + str(value/100) + "°C")


print("========================================")
r = eval(reqT.get('[8, 30, 10]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

value = r[0] << 8 | r[1]
print("daylength: \t\t" + str(value/0.016667) + " minutes")

value = r[2] << 8 | r[3]
print("nightlength: \t" + str(value/0.016667) + " minutes")

value = r[4] << 8 | r[5]
print("fanOnTimeTotal: " + str(value/0.016667) + " minutes")

value = r[6] << 8 | r[7]
print("fanOnTimeLast: \t" + str(value/0.016667) + " minutes")

value = r[8] << 8 | r[9]
print("fanOffTimeLast: " + str(value/0.016667) + " minutes")


print("========================================")
r = eval(reqT.get('[8, 40, 5]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

print("FanOn: " + str(r[0]))
print("day: " + str(r[1]))
print("chargingOn: " + str(r[2]))
print("pulsedregime: " + str(r[3]))
print("balancingOn: " + str(r[4]))


quit()





# humidity sensor:
# memory mapping:
# 5 = I2C-ID
# 6 = loop speed ms (x10)
# 7 & 8 = compressed floating point temperature sensor TOP --> ((id7-50) + (id8/100))
# 9 & 10 = compressed floating point relative humidity TOP --> (id9 + (id10/100))
# 11 & 12 = compressed floating point absolute humidity TOP
# 13 & 14 = compressed floating point temperature sensor BOT
# 15 & 16 = compressed floating point relative humidity BOT
# 17 & 18 = compressed floating point absolute humidity BOT

r = eval(reqT.get('[12, 5, 14]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

r = eval(reqT.get('[13, 5, 14]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()
quit()


reqT.get('0', "reset")          # set the master for WriteSlave
quit()
# humidity sensors:
#========================================================================
#r = eval(reqT.get('[13, 6, 1 , 25]', "WS"))

r = eval(reqT.get('[12, 5, 14]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

r = eval(reqT.get('[13, 5, 14]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

quit()


# PWm fan controller
# ========================================================================
reqT.get('[50, 6, 1, 75]', "WS")          # set the master for WriteSlave
r = eval(reqT.get('[50, 5, 10]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

quit()



# ===========================================================================
#reqT.get('[127, 5, 1, 13]', "WS")          # set the master for WriteSlave
#reqT.get('[12, 6, 1, 25]', "WS")          # set the master for WriteSlave

r = eval(reqT.get('[12, 5, 14]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()

r = eval(reqT.get('[13, 5, 14]', "RS"))
for i in range(len(r)):
    print(r[i], end=" ")
print()
quit()

reqT.get('["00", "13", "A2", "00", "41", "92", "F3", "9E"]', "setRFmode") # set wireless master mode
reqT.get('0', "clrRFmode")                 # read bus_memory from remote device

quit()

#reqT.get('["00", "00", "00", "00", "00", "00", "FF", "FF"]', "setRFmode") # set wireless master mode
#reqT.get('0', "clrRFmode")
#time.sleep(1)
reqT.get('[16, 2, 15, 10]', 'WM')
#reqT.get('0', "clrRFmode")                 # read bus_memory from remote device
#reqT.get('[16, 9, 13, 00, 19, 162, 00, 64, 134, 78, 220]', "WM") # set wireless master mode

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