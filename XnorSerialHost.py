import serial, time

class XnorSerialHost():
    def __init__(self, pPort, pBautrate=9600):
        self._connectionInit(pPort, pBautrate)

    def __del__(self):
        self.ser.close()

    def _connectionInit(self, pPort, pBautrate):
        print("Establishing serial connection to embedded device: ", end=" ")
        self.ser = serial.Serial(pPort, pBautrate, timeout=.5)
        time.sleep(2.5)
        self.ser.write(b'\x01')     # send SOH byte
        check = self.ser.read(2)    # check if device responds with ACK and EOT bytes
        if(check == b'\x06\x04'):
            print("OK")
        else:
            print(" ERROR")
            quit(1)

    def _sendRawData__bck(self, data):
        print("data test:")
        sendBytes = b'\x01'
        sendBytes += data
        print("sendBytes: ", sendBytes)
        self.ser.write(sendBytes)
        data = self.ser.read(8)
        print(len(data))
        print(data)

    def _sendRawData(self, pData, pDebug=False):
        retryCount = 3
        while(retryCount > 0):
            if( (len(pData) != pData[1] + 2)) and (len(pData) > 2):      # do not check for length on read action
                print("Write action data length error")
                return False

            # prepare to send data:
            sendBytes = b'\x01'
            sendBytes += bytes(pData)
            self.ser.write(sendBytes)

            # read received data:
            rcv = (self.ser.read(pData[1] + 2))

            # check validity of received data:
            isSuccess = True
            errorCode = 0
            if( ((len(rcv)) != pData[1] + 2)) and (len(pData) <= 2):   # do not check for length on write action
                errorCode = 1
                isSuccess = False
            if(rcv[0] != 6):
                errorCode = 2
                isSuccess = False
            if (rcv[-1] != 4):
                errorCode = 3
                isSuccess = False

            # determine what to do when data is corrupted:
            if(isSuccess == False):
                retryCount -= 1
                if(retryCount <= 0):
                    if(errorCode == 1):
                        print("Read action data length error")
                    if(errorCode == 2):
                        print("ACK error")
                    if(errorCode == 3):
                        print("EOT error")
                    return False
                else:
                    time.sleep(.1) # give hardware a break

            # if data is not corrupt, return the value
            else:
                return rcv[1:-1]  # chopchop the ACK and EOT chars


xsh = XnorSerialHost(pPort='/dev/ttyUSB1', pBautrate=19200)

xsh._sendRawData([6, 7, 2, 124, 0, 3, 0, 240, 15])
xsh._sendRawData([6, 7, 2, 125, 0, 3, 0, 240, 15])


eCount = 0
sCount = 0
startTime = time.time()
for o in range(0, 100):
    dataLib = []
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