import json, os

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

    # builds a device dictionary from the previously scanned IDList:
    def getDevicesInfoDict(self, pDevIdList, pDebug=False):

        # getting a jsonDictionary with supported devices and their names:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/devices.json') as f:
            supportedDevicesDictionary = json.load(f)

        # getting the hardware identifiers from each slave device:
        returnList = []
        for devId in pDevIdList:
            cmd = [devId, 0, 5]
            rcvBytes = eval(self.XRQ.get(str(cmd), "RS"))                   # set de master for ReadSlave

            # convert byte array to readable list:
            devInfoArr = []
            for i in range(0, len(rcvBytes)):
                devInfoArr.append(rcvBytes[i])

            deviceDict = {}
            deviceDict["I2C_ID"] = str(devId)
            deviceDict["HW_ID"] = str(devInfoArr[:-1]).replace(' ', '')
            deviceDict["FW_ID"] = " v" + str(devInfoArr[-1]).replace(' ', '')

            try:
                combiID = str(devInfoArr).replace(' ', '')
                deviceDict["DEV_TYPE"] = supportedDevicesDictionary["devices"][combiID]["DEV_TYPE"]
                deviceDict["DEV_PAGE"] = supportedDevicesDictionary["devices"][combiID]["DEV_PAGE"]
                deviceDict["URL"] = "DEV_PAGE=" + deviceDict["DEV_PAGE"] + '&' + "I2C_ID=" + deviceDict["I2C_ID"]
            except KeyError:
                deviceDict["DEV_TYPE"] = "UNKNOWN_DEVICE"
                deviceDict["DEV_PAGE"] = "UNKNOWN_DEVICE"
                deviceDict["URL"] = "DEV_PAGE=" + "devices/unsupported_device.html" + '&' + "I2C_ID=" + deviceDict["I2C_ID"]




            # print to debug console:
            if(pDebug):
                print(devId, ": ", end='\t')
                for i in range(0,5):
                    print(rcvBytes[i], end='\t')
                print(" - ", deviceDict["DEV_TYPE"], deviceDict["FW_ID"])

            returnList.append(deviceDict)
        return returnList