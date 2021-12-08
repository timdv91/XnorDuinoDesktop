import json, os, time
from pathlib import Path

class temporaryFileManager():
    def __init__(self, pFileName):
        self.FILENAME = pFileName

    # Store devicelist into tmp file:
    # ====================================================================================
    def writeDevListToFile(self, pDevList):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
        with open(dir_path + '/DB/TMP/' + self.FILENAME, 'w') as f:
            json.dump(pDevList, f, ensure_ascii=False, indent=4)

    # Store devicelist into tmp file:
    def readDevListFromFile(self):
        # getting a jsonDictionary with supported devices and their names:
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent)
        with open(dir_path + '/DB/TMP/' + self.FILENAME) as f:
            tmpDeviceList = json.load(f)
        return tmpDeviceList