import json, os, time

class xnorbusDAQ():
    def __init__(self, pXRQ, pFileName):
        self.XRQ = pXRQ
        self.FILENAME = pFileName

    def getConfigFromFile(self,):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/' + self.FILENAME) as f:
            daqConfig = json.load(f)
        return daqConfig