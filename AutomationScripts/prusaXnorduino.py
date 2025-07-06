import json, subprocess, requests

class PrusaAutomation:
    def __init__(self, pURL_Printer, pURL_Xnorduino):
        self.PRINTER_URL = pURL_Printer
        self.XNORDUINO_URL = pURL_Xnorduino

        prusaJsonDict = self._getPrinterData()
        if prusaJsonDict == None:
            print("Printer not online! Exiting...")
            quit()

        self._setFanController(prusaJsonDict)
        self._setLedController(prusaJsonDict)

    def _getPrinterData(self):
        # Read info from printer:
        cli = [
            "curl",
            "-H",
            "X-Api-Key: xxxxxxxxxxxxxxx",
            "-s",
            self.PRINTER_URL
        ]
        p = subprocess.run(cli, capture_output=True, text=True)
        dict = None
        if p.returncode == 0:
            dict = json.loads(p.stdout)
        return dict

    def _setFanController(self, pPrusaJsonDict):
        if pPrusaJsonDict == None:
            return

        nozzleTemp = pPrusaJsonDict["telemetry"]["temp-nozzle"]
        fanPWM = int(nozzleTemp * 1.28)
        if fanPWM < 64:
            fanPWM = 0
        elif fanPWM > 255:
            fanPWM = 255

        # Write data to xnorduino devices:
        reqT = requestTest(self.XNORDUINO_URL)
        r = eval(reqT.get('[22, 7, 1]', "RS"))  # Fan controller tends to be buggy, so we don't use cache reads here
        if r[0] < fanPWM - 5 or r[0] > fanPWM + 5:
            print("Fan value changed outside range, updating xnorduino system with new data.")
            newVal = [22, 7, 1]
            newVal.append(fanPWM)
            reqT.get(str(newVal), "WS")
        else:
            print("Fan value within range, no need for change.")


    def _setLedController(self, pPrusaJsonDict):
        if pPrusaJsonDict == None:
            return

        # Read rooflight intensity and temperature from gateway cache:
        reqT = requestTest(self.XNORDUINO_URL)
        roofLightIntensity = eval(reqT.get('[50, 12, 1]', "RSC"))[0]
        roofLightTemperature = eval(reqT.get('[50, 11, 1]', "RSC"))[0]

        # Set 3D printer light intensity and temperature:
        idleIntensity = 228
        printingIntensity = roofLightIntensity
        newVal_intensity = [21, 9, 1]
        newVal_temperature = [21, 10, 1]

        # Read printer light intensity and temperature from cache:
        printerLED_Intensity = eval(reqT.get(str(newVal_intensity), "RSC"))[0]
        printerLED_Temperature = eval(reqT.get(str(newVal_temperature), "RSC"))[0]

        # Update ledController slave module temperature setting:
        if int(printerLED_Temperature) != (roofLightTemperature):
            print("Updating light temperature setting.")
            newVal_temperature.append(roofLightTemperature)
            reqT.get(str(newVal_temperature), "WS")

        # Update ledController slave module intensity setting:
        isPrinting = pPrusaJsonDict["state"]["flags"]["printing"]
        if isPrinting == False and printerLED_Intensity != idleIntensity:
            print("Printing done, updating led light intensity.")
            newVal_intensity.append(idleIntensity)
            reqT.get(str(newVal_intensity), "WS")
        elif isPrinting == True and printerLED_Intensity != printingIntensity:
            print("Printing started, updating led light intensity.")
            newVal_intensity.append(printingIntensity)
            reqT.get(str(newVal_intensity), "WS")
        else:
            print("LED value already set, no need for changes.")
class requestTest():
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


PrusaAutomation(pURL_Printer="http://192.168.1.67:80/api/printer", pURL_Xnorduino="http://192.168.1.69:8080")
