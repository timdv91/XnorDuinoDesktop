import json, os, time
from pathlib import Path

class xnorbusDAQ():
    def __init__(self, pXRQ, pFileName):
        self.XRQ = pXRQ
        self.FILENAME = pFileName

    def readConfigFromFile(self):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
        with open(dir_path + '/CONFIG/' + self.FILENAME) as f:
            daqConfig = json.load(f)
        return daqConfig

    def writeConfigToFile(self, pData):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
        with open(dir_path + '/CONFIG/' + self.FILENAME, 'w') as f:
            json.dump(pData, f, ensure_ascii=False, indent=4)

