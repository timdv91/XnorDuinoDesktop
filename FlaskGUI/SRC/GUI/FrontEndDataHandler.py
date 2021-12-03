class DeviceListLoader():
    def __init__(self):
        None

    def dictKeyErrorCheck(self, pDevicesDictionary):
        try:
            t = pDevicesDictionary['SLAVES']
            t = pDevicesDictionary['MASTER']
        except KeyError:
            pDevicesDictionary['SLAVES'] = {}
            pDevicesDictionary['MASTER'] = {}

        return pDevicesDictionary

class TreeViewLoader():
    def __init__(self):
        None

    def dictKeyErrorCheck(self, pDevicesDictionary):
        try:
            t = pDevicesDictionary['SLAVES']
            t = pDevicesDictionary['MASTER']
        except KeyError:
            pDevicesDictionary['SLAVES'] = {}
            pDevicesDictionary['MASTER'] = {}

        return pDevicesDictionary

    def nestedDictParameterCleanup(self, pDevicesDictionary):
        # Clearing ugly parameters from Nested dictionary var:
        for i in range(0, len(pDevicesDictionary['SLAVES'])):
            if (str(type(pDevicesDictionary['SLAVES'][i]['NESTED'])) != "<class 'list'>"):
                pDevicesDictionary['SLAVES'][i]['NESTED'] = ""

        return pDevicesDictionary

    def addingNewNestedParameters(self, pDevicesDictionary):
        # adding a new parameter to dictionary var, to determine if the device has already been listed as nested device:
        for i in range(0, len(pDevicesDictionary['SLAVES'])):
            pDevicesDictionary['SLAVES'][i]['isNested'] = False  # set each device as not nested in list
        return pDevicesDictionary

    def retagPreviouslyNestedDevices(self, pDevicesDictionary):
        # check what devices have previously been listed as nested devices, tag them:
        for i in range(0, len(pDevicesDictionary['SLAVES'])):
            for o in range(0, len(pDevicesDictionary['SLAVES'][i]['NESTED'])):
                # print(devicesDictionary['SLAVES'][i]['NESTED'][o])
                for p in range(0, len(pDevicesDictionary['SLAVES'])):
                    # print("\t", devicesDictionary['SLAVES'][p]['I2C_ID'], end=" ")
                    if (int(pDevicesDictionary['SLAVES'][i]['NESTED'][o]) == int(
                            pDevicesDictionary['SLAVES'][p]['I2C_ID'])):
                        pDevicesDictionary['SLAVES'][p]['isNested'] = True  # set specific devices as listed in list
                        # print("- detected")
                        break
                    # print()
        return pDevicesDictionary

# ==================================

class DevicesPageLoader():
    def __init__(self, pRequest):
        self.request = pRequest

    def dataLoader(self):
        posts = {}
        if self.request.method == 'GET':
            posts['DEV_TYPE'] = self.request.args['DEV_TYPE']
            posts['DEV_PAGE'] = self.request.args['DEV_PAGE']
            posts['I2C_ID'] = self.request.args['I2C_ID']
            posts['HW_ID'] = self.request.args['HW_ID']
            posts['FW_ID'] = self.request.args['FW_ID']
        return posts

class DevicesPageWriter():
    def __init__(self, pRequest):
        self.request = pRequest

    def getRequestData(self):
        posts = {}
        send_startId = None
        send_n = None
        if self.request.method == 'GET':
            posts = eval(self.request.args.getlist('posts')[0])  # Why inside an array? Check this later on?
            send_startId = eval(self.request.args.getlist('cmd')[0])[0]
            send_n = eval(self.request.args.getlist('cmd')[0])[1]
        return posts, send_startId, send_n

    def getErrorCheck(self, pSend_n):
        isValid = True
        sendValue = ""
        if self.request.method == 'GET':
            for i in range(0, pSend_n):
                nr = self.request.args.getlist(str(i))[0]
                sendValue += ", " + str(nr)
                try:
                    if int(nr) < 0 or int(nr) > 255:
                        isValid = False
                except ValueError:
                    isValid = False
        return sendValue, isValid

    def getWriteCommand(self, pPosts, pSend_startId, pSend_n, pSendValue):
        cmd = None
        writeMethod = None

        if self.request.method == 'GET':
            I2C_ID = pPosts['I2C_ID']
            if (I2C_ID != '0'):
                cmd = "[" + str(I2C_ID) + ", " + str(pSend_startId) + ", " + str(pSend_n) + "" + str(pSendValue) + "]"
                writeMethod = 'WS'
            else:
                cmd = "[" + str(pSend_startId) + ", " + str(pSend_n) + "" + str(pSendValue) + "]"
                writeMethod = 'WM'

        print(cmd, writeMethod)                          # last comma is automatically put in place!
        return cmd, writeMethod

    def executeWriteCommand(self, pXRQ, pCmd, pWriteMethod, pIsValid):
        if self.request.method == 'GET':
            if pIsValid:
                print("Valid input!", pWriteMethod)
                rcvBytes, commErrorCount = pXRQ.get(str(pCmd), pWriteMethod)  # set de master for ReadSlave
                print(rcvBytes, commErrorCount)
            else:
                print("Invalid input!")