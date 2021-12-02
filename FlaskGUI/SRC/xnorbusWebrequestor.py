import requests, time

ERR_COUNT_MAX = 10

class xnorbusWebrequestor():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        try:
            ErrorCounter = ERR_COUNT_MAX
            while(True):
                r = requests.get(str(self.URL + "/" + pPath), data=(pData))
                hasError = self.hasCommError(r)

                if(hasError == False or ErrorCounter == 0):
                    return r.text, (ERR_COUNT_MAX - ErrorCounter)
                else:
                    ErrorCounter -= 1
                    time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            return None, 0


    def post(self, pData, pPath=""):
        # POST request:
        try:
            ErrorCounter = ERR_COUNT_MAX
            while(True):
                r = requests.post(str(self.URL + "/" + pPath), data=(pData))
                hasError = self.hasCommError(r)

                if(hasError == False or ErrorCounter == 0):
                    return r.text, (ERR_COUNT_MAX - ErrorCounter)
                else:
                    ErrorCounter -= 1
                    time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            return None, 0


    def hasCommError(self, pR):
        if(pR != None):
            if(len(eval(pR.text)) <= 2):
                errorList = []
                #errorList.append(b'\x00\x00')
                errorList.append(b'\x00\x18')
                errorList.append(b'\x00\x06')
                errorList.append(b'\x00\x04')
                errorList.append(b'\x00\x07')

                if(pR.text in str(errorList)):
                    print("COMM-ERROR detected: ", pR.text)
                    return True

        return False