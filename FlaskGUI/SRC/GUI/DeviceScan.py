
class DeviceScan():
    def __init__(self, pXRH):
        self.XRH = pXRH
        self.commErrorCount = 0

    def getMasterInfo(self, pCommonDataStruct):
        print("Hardware communication: Started")
        dataStructMaster, commErrorCount = self.XRH.getMasterInformation()


        if (self.commErrorCount == 0):
            pCommonDataStruct['MASTER'] = dataStructMaster  # copy from buffer into main struct
        else:
            pCommonDataStruct = {}                          # clear main hardware struct when master doesn't response
        return pCommonDataStruct

    def getMasterSlavesIdList(self, pCommonDataStruct):
        # Scan slave devices only when supported by device (named 'MASTER'):
        devIdList = []
        if (pCommonDataStruct['MASTER']['DEV_TYPE'] == 'Master'):
            devIdList, self.commErrorCount = self.XRH.initDeviceIDScan()
        return devIdList

    def getSlavesInfo(self, pDevIdList):
        devicesDictionary = None
        if (self.commErrorCount == 0):  # do not check 'devIdList = None', it could prevent non master devices from being shown in the GUI.
            devicesDictionary, self.commErrorCount = self.XRH.getDevicesInfoDict(pDevIdList, pDebug=False)
        return devicesDictionary

    def getNestingChildDevices(self, pCommonDataStruct, pDevicesDictionary):
        if (self.commErrorCount == 0 and pDevicesDictionary != None):
            commonDataStructSlaves, self.commErrorCount = self.XRH.getDevicesNestingDict(pDevicesDictionary['SLAVES'], pDebug=False)
            if (self.commErrorCount == 0 and commonDataStructSlaves != None):
                pCommonDataStruct['SLAVES'] = commonDataStructSlaves  # only update main struct when all errorchecks have passed
        return pCommonDataStruct

    def getErrorStats(self):
        return self.commErrorCount