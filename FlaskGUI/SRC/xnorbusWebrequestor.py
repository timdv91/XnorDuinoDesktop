import requests, time

class xnorbusWebrequestor():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        try:
            counter = 11
            while(True):
                counter -= 1

                r = requests.get(str(self.URL + "/" + pPath), data=(pData))
                hasError = self.hasCommError(r)

                if(hasError == False or counter == 0):
                    return r.text, counter
                else:
                    time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            return None, 0


    def post(self, pData, pPath=""):
        # POST request:
        try:
            counter = 10
            while(True):
                counter -= 1

                r = requests.post(str(self.URL + "/" + pPath), data=(pData))
                hasError = self.hasCommError(r)

                if(hasError == False or counter == 0):
                    return r.text, counter
                else:
                    time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            return None, 0


    def hasCommError(self, pR):
        if(pR != None):
            if(len(eval(pR.text)) <= 2):
                errorList = []
                errorList.append(b'\x00\x00')
                errorList.append(b'\x00\x18')
                errorList.append(b'\x00\x06')
                errorList.append(b'\x00\x04')
                errorList.append(b'\x00\x07')

                if(pR.text in str(errorList)):
                    print("COMM-ERROR detected: ", pR.text)
                    return True

        return False