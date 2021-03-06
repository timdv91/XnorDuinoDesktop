import json, os, time
from pathlib import Path

class xnorbusRequestorHelper():
    def __init__(self, pXRQ, pFileName):
        self.XRQ = pXRQ
        self.FILENAME = pFileName

    def getMasterInformation(self):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
        with open(dir_path + '/CONFIG/' + self.FILENAME) as f:
            supportedDevicesDictionary = json.load(f)

        retVal = {}
        commErrorCount = 0
        try:
            # requesting data from master:
            data, commErrorCount = self.XRQ.get('[0,14]', "RM")
            rcvBytes = eval(data)

            rcv = []
            for i in range(len(rcvBytes)):
                rcv.append(rcvBytes[i])

            # moving data in it's place:
            retVal['I2C_ID'] = str(0)
            retVal['HW_ID'] = str(rcv[0:4])
            retVal['FW_ID'] = 'v' + str(rcv[4:5][0])
            retVal['ALERT'] = str(rcv[5:6][0])
            retVal['PM_IC'] = str(rcv[6:10])
            retVal['TRM_MOD'] = str(rcv[10:14])

            try:
                combiID = str(rcv[0:5]).replace(' ', '')
                retVal["DEV_TYPE"] = supportedDevicesDictionary["MASTER"][combiID]["DEV_TYPE"]
                retVal["DEV_PAGE"] = supportedDevicesDictionary["MASTER"][combiID]["DEV_PAGE"]
                retVal["MEM_MAP"] = supportedDevicesDictionary["MASTER"][combiID]["MEM_MAP"]
                retVal["WINDOW_SIZE"] = supportedDevicesDictionary["MASTER"][combiID]["WINDOW_SIZE"]
                retVal["URL"] = "DEV_PAGE=" + retVal["DEV_PAGE"] \
                                    + '&' + "I2C_ID=" + '0' \
                                    + '&' + "DEV_TYPE=" + retVal["DEV_TYPE"] \
                                    + '&' + "HW_ID=" + retVal["HW_ID"] \
                                    + '&' + "FW_ID=" + retVal["FW_ID"]
            except KeyError:
                retVal["DEV_TYPE"] = "UNKNOWN_DEVICE"
                retVal["DEV_PAGE"] = "UNKNOWN_DEVICE"
                retVal["MEM_MAP"] = "UNKNOWN_DEVICE"
                retVal["WINDOW_SIZE"] = [350, 300]
                retVal["URL"] = "DEV_PAGE=" + "devices/unsupported_device.html" \
                                    + '&' + "I2C_ID=" + '0' \
                                    + '&' + "DEV_TYPE=" + retVal["DEV_TYPE"] \
                                    + '&' + "HW_ID=" + retVal["HW_ID"] \
                                    + '&' + "FW_ID=" + retVal["FW_ID"]
        except IndexError:
            print("IndexError getMaster, resetting hardware")
            self.XRQ.get('[0,0]', "reset")
        except TypeError:
            print("TypeError getMaster, resetting hardware")
            self.XRQ.get('[0,0]', "reset")
        except Exception as e:
            print(str(e) + ",  returning 'None' value")
            self.XRQ.get('[0,0]', "reset")

        return retVal, commErrorCount

    # uses the scan function (function 3) implemented on the master_embedded device to scan for slaves:
    def initDeviceIDScan(self, pDebug=False):
        retVal = []
        divScanCount = 12
        commErrorCountTotal = 0
        try:
            for dev in range(1, 127, divScanCount):
                scanList = [16, 3, 3, dev, dev+divScanCount]
                self.XRQ.get(str(scanList), "WM")

                data, commErrorCount = self.XRQ.get('[21,9]', "RM")
                rcv = eval(data)
                commErrorCountTotal += commErrorCount

                for i in range(len(rcv)):
                    if (rcv[i] != 0 and rcv[i] < 128):
                        retVal.append(rcv[i])

                if(pDebug):
                    print(dev, "-", dev + (divScanCount - 1), " : ", end="\t")
                    for i in range(len(rcv)):
                        print(rcv[i], end='\t')
                    print("")
        except TypeError as e:
            print(str(e) + ",  returning 'None' value")
            return None, -1
        except Exception as e:
            print(str(e) + ",  returning 'None' value")
            return None, -1

        return retVal, commErrorCountTotal

    # builds a device dictionary from the previously scanned IDList:
    def getDevicesInfoDict(self, pDevIdList, pDebug=False):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
        with open(dir_path + '/CONFIG/' + self.FILENAME) as f:
            supportedDevicesDictionary = json.load(f)

        # getting the hardware identifiers from each slave device:
        returnDict = {}
        devicesList = []
        commErrorCountTotal = 0
        for devId in pDevIdList:
            try:
                cmd = [devId, 0, 5]
                data, commErrorCount = self.XRQ.get(str(cmd), "RS")                   # set de master for ReadSlave
                rcvBytes = eval(data)
                commErrorCountTotal += commErrorCount

                # convert byte array to readable list:
                devInfoArr = []
                for i in range(0, len(rcvBytes)):
                    devInfoArr.append(rcvBytes[i])

                deviceDict = {}
                deviceDict["I2C_ID"] = str(devId)
                deviceDict["HW_ID"] = str(devInfoArr[:-1]).replace(' ', '')
                deviceDict["FW_ID"] = "v" + str(devInfoArr[-1]).replace(' ', '')
            except IndexError as e:
                print(str(e) + ",  returning 'None' value")
                return None
            except Exception as e:
                print(str(e) + ",  returning 'None' value")
                return None

            try:
                combiID = str(devInfoArr).replace(' ', '')
                deviceDict["DEV_TYPE"] = supportedDevicesDictionary["SLAVES"][combiID]["DEV_TYPE"]
                deviceDict["DEV_PAGE"] = supportedDevicesDictionary["SLAVES"][combiID]["DEV_PAGE"]
                deviceDict["MEM_MAP"] = supportedDevicesDictionary["SLAVES"][combiID]["MEM_MAP"]
                deviceDict["WINDOW_SIZE"] = supportedDevicesDictionary["SLAVES"][combiID]["WINDOW_SIZE"]
                deviceDict["DEV_NESTING"] = supportedDevicesDictionary["SLAVES"][combiID]["DEV_NESTING"]
                deviceDict["URL"] = "DEV_PAGE=" + deviceDict["DEV_PAGE"] \
                                    + '&' + "I2C_ID=" + deviceDict["I2C_ID"] \
                                    + '&' + "DEV_TYPE=" + deviceDict["DEV_TYPE"] \
                                    + '&' + "HW_ID=" + deviceDict["HW_ID"] \
                                    + '&' + "FW_ID=" + deviceDict["FW_ID"]
            except KeyError:
                deviceDict["DEV_TYPE"] = "UNKNOWN_DEVICE"
                deviceDict["DEV_PAGE"] = "UNKNOWN_DEVICE"
                deviceDict["MEM_MAP"] = "UNKNOWN_DEVICE"
                deviceDict["WINDOW_SIZE"] = [350, 300]
                deviceDict["DEV_NESTING"] = -1
                deviceDict["URL"] = "DEV_PAGE=" + "devices/unsupported_device.html" \
                                    + '&' + "I2C_ID=" + deviceDict["I2C_ID"] \
                                    + '&' + "DEV_TYPE=" + deviceDict["DEV_TYPE"] \
                                    + '&' + "HW_ID=" + deviceDict["HW_ID"] \
                                    + '&' + "FW_ID=" + deviceDict["FW_ID"]

            except Exception as e:
                print(str(e) + ",  Unexpected error occurred.")

            # print to debug console:
            if(pDebug):
                print(devId, ": ", end='\t')
                for i in range(0,5):
                    print(rcvBytes[i], end='\t')
                print(" - ", deviceDict["DEV_TYPE"], deviceDict["FW_ID"])

            devicesList.append(deviceDict)

        returnDict['SLAVES'] = devicesList
        return returnDict, commErrorCountTotal


    def getDevicesNestingDict(self, pDevicesDict, pDebug=False):
        devicesDictLocal = pDevicesDict
        debugPrint = ""
        commErrorCountTotal = 0
        for i in range(0, len(pDevicesDict)):
            device = pDevicesDict[i]
            debugPrint += "Device: " + str(device["DEV_TYPE"]) + "\n"
            if (device["DEV_NESTING"] < 0):
                debugPrint += "\tNestign support: NO" + "\n"
                devicesDictLocal[i]["NESTED"] = "N/A"
            else:
                try:
                    debugPrint += "\tNesting support: YES" + "\n"
                    cmd = [int(device["I2C_ID"]), int(device["DEV_NESTING"]), 1]
                    data, commErrorCount = self.XRQ.get(str(cmd), "RS")  # set de master for ReadSlave
                    rcvBytes = eval(data)
                    commErrorCountTotal += commErrorCount

                    debugPrint += "\tConnected slave devices:" + str(int(rcvBytes[0])) + "\n"
                    if(int(rcvBytes[0]) > 0):
                        cmd = [int(device["I2C_ID"]), int(device["DEV_NESTING"])+1, int(rcvBytes[0])]
                        data, commErrorCount = self.XRQ.get(str(cmd), "RS")  # set de master for ReadSlave
                        nestedDevIdList_bytes = eval(data)
                        commErrorCountTotal += commErrorCount

                        debugPrint += "\tConnected slaves ID's: "
                        nestedDevIdList = []
                        for ids in nestedDevIdList_bytes:
                            nestedDevIdList.append(ids)
                            debugPrint += str(ids) + ' '
                        debugPrint += "\n"
                        devicesDictLocal[i]["NESTED"] = nestedDevIdList
                    else:
                        devicesDictLocal[i]["NESTED"] = "None"
                except IndexError as e:
                    print(str(e) + ",  returning 'None' value")
                    devicesDictLocal[i]["NESTED"] = "None"
                except Exception as e:
                    print(str(e) + ",  returning 'None' value")
                    devicesDictLocal[i]["NESTED"] = "None"

        if(pDebug):
            print(str(debugPrint))
        return devicesDictLocal, commErrorCountTotal



