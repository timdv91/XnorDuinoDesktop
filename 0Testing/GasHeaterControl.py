import json, subprocess, requests
import time


class requestXnorbus():
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

class requestXbee():
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


class GasHeater():
    def __init__(self):
        self.RXBEE = requestXbee("http://192.168.2.9:8082")
        self.REMOTE_DEV = "0013A20041BD0FD5"

    def getHeaterState(self):
        ssrOn = self.RXBEE.get('["' + self.REMOTE_DEV + '","get_io_configuration()","IOLine.DIO3_AD3"]', "R")

        if ssrOn == "IOMode.DIGITAL_OUT_LOW":
            return False
        elif ssrOn == "IOMode.DIGITAL_OUT_HIGH":
            return True
        return None

    def setHeaterState(self, pRelayState):
        # Turn heater on/off:
        if pRelayState == True:
            r = self.RXBEE.get('["' + self.REMOTE_DEV + '","set_io_configuration()","IOLine.DIO3_AD3", "IOMode.DIGITAL_OUT_HIGH"]', "W")
        else:
            r = self.RXBEE.get('["' + self.REMOTE_DEV + '","set_io_configuration()","IOLine.DIO3_AD3", "IOMode.DIGITAL_OUT_LOW"]', "W")
        return r

    def getConnectedState(self):
        ssrOn = self.RXBEE.get('["' + self.REMOTE_DEV + '","get_io_configuration()","IOLine.DIO2_AD2"]', "R")
        if ssrOn == "False":
            return False
        else:
            return True


class XnorBUS():
    def __init__(self):
        self.RXBUS = requestXnorbus("http://192.168.2.9:8080")

    def getTerminationTemperature(self):
        # Write data to xnorduino devices:
        r = eval(self.RXBUS.get('[126, 9, 1]', "RS"))
        value = int.from_bytes(r, byteorder='big')
        return value


class Main():
    def __init__(self, pSetPoint = 18):
        self.SETPOINT = pSetPoint

    def tempGuard(self):
        GH = GasHeater()
        TT = XnorBUS()

        if GH.getConnectedState() == False:
            print("Error connecting to gas heater!")
            return

        temp = TT.getTerminationTemperature()
        if temp == 0:
            print("Error connecting to temp sensor!")
            return

        print("Setpoint temperature: ", self.SETPOINT ,"°C")
        print("Current temperature:  ", temp ,"°C")
        if temp < self.SETPOINT and GH.getHeaterState() == False:
            print("\t- Action required -> Turning on gas heater!")
            GH.setHeaterState(True)
        elif temp > self.SETPOINT and GH.getHeaterState() == True:
            print("\t- Action required -> Turning off gas heater!")
            GH = GasHeater()
            GH.setHeaterState(False)
        else:
            print("\t - No actions required, heater is ", end="")
            if GH.getHeaterState() == True:
                print("on!")
            else:
                print("off!")



main = Main()
while True:
    main.tempGuard()
    time.sleep(30)