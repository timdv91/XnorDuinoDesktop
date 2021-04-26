import serial, time

class XnorSerialHost():
    def __init__(self, pPort, pBautrate=38400):
        self._connectionInit(pPort, pBautrate)
        self.isComLocked = False

    def __del__(self):
        self.ser.close()

    def _connectionInit(self, pPort, pBautrate):
        print("Establishing serial connection to embedded device: ", end=" ")
        self.ser = serial.Serial(pPort, pBautrate, timeout=.25)
        time.sleep(2.5)
        self.ser.write(b'\x01')     # send SOH byte
        check = self.ser.read(2)    # check if device responds with ACK and EOT bytes
        if(check == b'\x06\x04'):
            print("OK")
        else:
            print(" ERROR")
            quit(1)


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
        return retVal


    def rawCommunication(self, pData, pDebug=False):
        time.sleep(.02)
        if ((len(pData) != pData[1] + 2)) and (len(pData) > 2):  # do not check for length on read action
            print("Write action data length error!")              # Avoid writing invalid data to hardware
            return b'\x00\x00'                                   # send ascii null null

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
        print("Sending data: ", end=": ")
        print(pData)
        sendBytes = bytes(pData)
        self.ser.write(sendBytes)


        rcv = None
        if(len(pData) > 2): # read received data from write action:
            rcv = (self.ser.read(2))
        else: # read received data from data request:
            rcv = (self.ser.read(pData[1] + 1))
        print("received data: " , end=": ")
        print(rcv)

        # check for EOT byte:
        if(rcv[-1:] != b'\x04'):
            print("No EOT received from device error!")
            self.isComLocked = False
            return b'\x00\x04'                  # If EOT never received, abort send ascii null and EOT (EOT error)

        # Return received data if everything went successfully:
        print("Request processed successfully!")
        self.isComLocked = False
        return rcv[:-1]                         # chopchop the EOT char


    def readSlave(self, pData, pDebug=False):
        # first set the masters registers to init a read request on a slave:
        pData.insert(0, 16)     # start writing master register at index 16
        pData.insert(1, 4)       # inform master we're gonna write 4 bytes
        pData.insert(2, 1)      # set masters register to read request from slave
        print(pData)
        retval = self.rawCommunication(pData)

        # second read masters data register for data received from slave:
        print(pData[-1])
        retval = self.rawCommunication([20, 12])
        return retval

    def readMaster(self, pData, pDebug=False):
        return self.rawCommunication(pData)

    def writeSlave(self, pData, pDebug=False):
        # first set the masters registers to init a read request on a slave:
        dataSize = len(pData) + 1
        pData.insert(0, 16)  # start writing master register at index 16
        pData.insert(1, dataSize)  # inform master we're gonna write 4 bytes
        pData.insert(2, 2)  # set masters register to read request from slave
        print(pData)
        retval = self.rawCommunication(pData)
        return retval

    def writeMaster(self, pData, pDebug=False):
        if(pData[0] <= 8):           # master is only writable starting from index 9!
            return b'\x00\x00'
        return self.rawCommunication(pData)

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