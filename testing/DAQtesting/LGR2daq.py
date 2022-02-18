import requests
import json
import time

class XnorBusRequester():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        r = requests.get(str(self.URL + "/" + pPath), data=(pData))
        return r.text

    def post(self, pData, pPath=""):
        # POST request:
        r = requests.post(str(self.URL + "/" + pPath), data=(pData))
        return r.text

class HumidityLogger():
    def __init__(self):
        self.REQ = XnorBusRequester('http://127.0.0.1:8080')

        jsonArr = []
        jsonArr.append(self.getSensorData(46))
        jsonArr.append(self.getSensorData(55))

        # Directly from dictionary
        with open('../testing/DAQtesting/json/' + str(int(time.time())) + '.json', 'w') as outfile:
            json.dump(jsonArr, outfile, indent=4)


    def getSensorData(self, sID):
        r = eval(self.REQ.get('[' + str(sID) + ', 0, 13]', "RS"))

        sHWID = str(r[0]) + str(r[1]) + str(r[2]) + str(r[3])
        sFWID = str(r[4])
        sID = r[5]
        sTemp = (r[7]-50) + (r[8]/100)
        sRelH = r[9] + (r[10]/100)
        sAbsH = r[11] + (r[12]/100)

        print(sHWID)
        print(sFWID)
        print(sID)
        print(sTemp)
        print(sRelH)
        print(sAbsH)

        jsonVar =  {
            "measurement": "LGR2",
            "tags": {
                "name": "HumiditySensors",
                "HWv": sHWID,
                "FWv": sFWID,
                "sID": sID
            },
            "time": int(time.time()) * 1000000000,
            "fields": {
                "sTemp":sTemp,
                "sRelH":sRelH,
                "sAbsH":sAbsH
            }
        }

        return jsonVar

# humidity sensor:
# memory mapping:
# 5 = I2C-ID
# 6 = loop speed ms (x10)
# 7 & 8 = compressed floating point temperature sensor TOP --> ((id7-50) + (id8/100))
# 9 & 10 = compressed floating point relative humidity TOP --> (id9 + (id10/100))
# 11 & 12 = compressed floating point absolute humidity TOP
# 13 & 14 = compressed floating point temperature sensor BOT
# 15 & 16 = compressed floating point relative humidity BOT
# 17 & 18 = compressed floating point absolute humidity BOT
