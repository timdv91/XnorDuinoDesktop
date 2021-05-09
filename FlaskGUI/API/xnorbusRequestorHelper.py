import time

class xnorbusRequestorHelper():
    def __init__(self, pXRQ):
        self.XRQ = pXRQ

    # uses the scan function (function 3) implemented on the master_embedded device to scan for slaves:
    def initDeviceIDScan(self, pDebug=False):
        retVal = []
        for dev in range(1, 127, 9):
            scanList = [16, 3, 3, dev, dev+9]
            self.XRQ.get(str(scanList), "WM")
            rcv = eval(self.XRQ.get('[21,9]', "RM"))

            for i in range(len(rcv)):
                if (rcv[i] != 0):
                    retVal.append(rcv[i])

            if(pDebug):
                print(dev, "-", dev + (9 - 1), " : ", end="\t")
                for i in range(len(rcv)):
                    print(rcv[i], end='\t')
                print("")
        return retVal

    # builds a dictionary with basic information about each connected device:
    def getDevicesInfoDict(self, pDevIdList):
        for dev in pDevIdList:
            print(dev)

            '''
            this function should request the HW identifier of each connected slave device.
            the hardware identifier should then be compared to a list containing a naming scheme for each slave device.
            
            '''