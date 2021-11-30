'''
error codes:
    b'\x00\x00' --> write action, data length error / Writing master at wrong index location
    b'\x00\x18' --> communication locked by another thread
    b'\x00\x06' --> No ACK received from device error!
    b'\x00\x04' --> No EOT received from device error!
    b'\x00\x07' --> Unknown error / connection to hardware error            --> restarts serial connection to hardware
'''

import serial, time, copy
DEV_MODE = False

class XnorSerialHost():
    def __init__(self, pPort, pBautrate=38400):
        self.PORT = pPort
        self.BAUT = pBautrate
        self.isConnectedHW = False
        self.isComLocked = True
        self.RFmode = False
        self.RFMAC = None
        self.resetTimeout = time.time()

    def __del__(self):
        self.ser.close()

    def getHWConnectionState(self):
        return self.isConnectedHW

    def _connectionInit(self):
        pPort = self.PORT
        pBautrate = self.BAUT

        try:
            print("Establishing serial connection to embedded device: ", end=" ")
            self.ser = serial.Serial(pPort, pBautrate, timeout=.250)
            time.sleep(2.5)
            self.ser.write(b'\x01')     # send SOH byte
            check = self.ser.read(2)    # check if device responds with ACK and EOT bytes
            if(check == b'\x06\x04'):
                print("OK")

                self.ser.flushInput()
                self.ser.flushOutput()

                self.isComLocked = False
                self.isConnectedHW = True

                self.RFmode = False
                if(self.RFMAC != None):
                    print("Reconnecting to wireless device.")
                    self.setRFmode(self.RFMAC)

                return True
            else:
                print("ERROR ACK and/or EOT byte error upon connection!")
                self.isConnectedHW = False
                return b'\x00\x07'
        except Exception as e:
            print(str(e))

        self.ser.close()
        self.isConnectedHW = False
        return b'\x00\x07'
        # quit(1)     #Todo: remove quit, try to reconnect to hardware

    def _communication(self, pFunction , pData, pDebug=False):
        retVal = b'\x00\x00'
        if(pFunction == "/"):
            retVal = self.rawCommunication(pData)
        elif(pFunction == "/RS"):
            retVal = self.readSlave(pData)
        elif(pFunction == "/RM"):
            retVal = self.readMaster(pData)
        elif(pFunction == "/WS"):
            retVal = self.writeSlave(pData)
        elif(pFunction == "/WM"):
            retVal = self.writeMaster(pData)
        elif(pFunction == "/setRFmode"):
            retVal = self.setRFmode(pData)
        elif (pFunction == "/clrRFmode"):
            retVal = self.clrRFmode(pData)
        elif (pFunction == "/reset"):
            retVal = self.resetMode(pData)
        return retVal


    def rawCommunication(self, pData, pDebug=False):
        try:
            time.sleep(.02)
            if ((len(pData) != pData[1] + 2)) and (len(pData) > 2):  # do not check for length on read action
                print("Write action data length error!")             # Avoid writing invalid data to hardware
                return b'\x00\x00'                                   # send ascii null null

            if(self.isConnectedHW == False):
                print("Hardware not connected!")  # Avoid writing invalid data to hardware
                return b'\x00\x00'

            #Lock this function when active:
            if(self.isComLocked == True):
                print("Communication locked by another thread or process!")
                return b'\x00\x18'                  # Send ascii null and cancel (byte 24).

            self.isComLocked = True                 # Make sure each exits from this function resets this flag !!!

            # Start handshaking:
            sendBytes = b'\x01'
            self.ser.write(sendBytes)               # Send SOT byte.
            check = self.ser.read(1)                # Wait for ACK byte
            if (check != b'\x06'):
                print("No ACK received from device error!")
                self.isComLocked = False
                return b'\x00\x06'                  # If ACK never received, abort send ascii null and ack (ack error)


            # Send the command data after hardware ACK response:
            if(DEV_MODE):
                print("Sending data: ", end=": ")
                print(pData)
            sendBytes = bytes(pData)
            self.ser.write(sendBytes)


            rcv = None
            if(len(pData) > 2): # read received data from write action:
                rcv = (self.ser.read(2))
            else: # read received data from data request:
                rcv = (self.ser.read(pData[1] + 1))
            if(DEV_MODE):
                print("received data: " , end=": ")
                print(rcv)

            # check for EOT byte:
            if(rcv[-1:] != b'\x04'):
                print("No EOT received from device error!")
                self.isComLocked = False
                return b'\x00\x04'                  # If EOT never received, abort send ascii null and EOT (EOT error)

            # Return received data if everything went successfully:
            if(DEV_MODE):
                print("Request processed successfully!")
            self.isComLocked = False
            return rcv[:-1]                         # chopchop the EOT char
        except Exception as e:
            print(str(e))                           # todo: Add error message to a log file!

            self.ser.close()
            self.isConnectedHW = False

            return b'\x00\x07'                      # unknown error or connection reset

    def readSlave(self, pData, pDebug=False):
        # first set the masters registers to init a read request on a slave:
        pData.insert(0, 16)     # start writing master register at index 16
        pData.insert(1, 4)       # inform master we're gonna write 4 bytes
        pData.insert(2, 1)      # set masters register to read request from slave

        if (self.RFmode == True):
            dataSize = len(pData) + 1
            pData.insert(0, 16)
            pData.insert(1, dataSize)
            pData.insert(2, 11)

        if(DEV_MODE):
            print(pData)
        retval = self.rawCommunication(pData)

        if (self.RFmode == True):
            pDataSize = pData[-1]
            pData = []
            pData.insert(0, 16)
            pData.insert(1, 3)
            pData.insert(2, 12)
            pData.insert(3, 20)
            pData.insert(4, pDataSize)
            self.rawCommunication(pData)

        # second read masters data register for data received from slave:
        if(DEV_MODE):
            print(pData[-1])
        retval = self.rawCommunication([20, int(pData[-1])])
        return retval

    def readMaster(self, pData, pDebug=False):
        if(self.RFmode == True):
            pData.insert(0, 16)
            pData.insert(1, 3)
            pData.insert(2, 12)
            self.rawCommunication(pData)
            pData = [20, pData[4]]

        return self.rawCommunication(pData)

    def writeSlave(self, pData, pDebug=False):
        # first set the masters registers to init a read request on a slave:
        dataSize = len(pData) + 1
        pData.insert(0, 16)             # start writing master register at index 16
        pData.insert(1, dataSize)       # inform master we're gonna write 4 bytes
        pData.insert(2, 2)              # set masters register to read request from slave

        if (self.RFmode == True):
            dataSize = len(pData) + 1
            pData.insert(0, 16)
            pData.insert(1, dataSize)
            pData.insert(2, 11)

        if(DEV_MODE):
            print(pData)
        retval = self.rawCommunication(pData)
        return retval

    def writeMaster(self, pData, pDebug=False):
        if(pData[0] <= 4):           # master is only writable starting from index 9!
            return b'\x00\x00'

        if(self.RFmode == True):
            dataSize = len(pData) + 1
            pData.insert(0, 16)
            pData.insert(1, dataSize)
            pData.insert(2, 11)

        if(DEV_MODE):
            print(pData)
        return self.rawCommunication(pData)

    def setRFmode(self, pData):
        # create mac backup:
        self.RFMAC = copy.deepcopy(pData)

        # hex to dec conversion:
        for i in range(0,len(pData)):
            pData[i] = int(pData[i], 16)

        # first set the masters registers to init a read request on a slave:
        dataSize = len(pData) + 1
        pData.insert(0, 16)  # start writing master register at index 16
        pData.insert(1, dataSize)  # inform master we're gonna write n bytes
        pData.insert(2, 9)
        if(DEV_MODE):
            print(pData)
        retval = self.rawCommunication(pData)
        self.RFmode = True
        return retval

    def clrRFmode(self, pData):
        pData = []
        pData.insert(0, 16)  # start writing master register at index 16
        pData.insert(1, 1)
        pData.insert(2, 10)
        retval = self.rawCommunication(pData)

        self.RFmode = False
        self.RFMAC = None   # clear mac backup

        return retval

    def resetMode(self, pData):
        if(time.time() < self.resetTimeout + 15):
            print("Manual or automated connection reset canceled, to fast reoccurring...")
            return None

        print("Manual or automated connection reset requested...")
        self.ser.close()
        self.isConnectedHW = False

        self.resetTimeout = time.time()
        return b'\x00\x07'  # unknown error or connection reset

'''
xsh = XnorSerialHost(pPort='/dev/ttyUSB0', pBautrate=19200)

xsh._sendRawData([6, 7, 2, 124, 0, 3, 0, 240, 5])
xsh._sendRawData([6, 7, 2, 125, 0, 3, 0, 240, 5])

dataLib = []
eCount = 0
sCount = 0
startTime = time.time()

for i in range(0, 100):
    d = xsh._sendRawData([0, 6])
    if(d != False):
        dataLib.append(d)
        sCount += 1
    else:
        eCount += 1

print(dataLib)
print("Errors: ", eCount, end=" | ")
print("Success: ", sCount)
print("--- %s seconds ---" % (time.time() - startTime))
'''