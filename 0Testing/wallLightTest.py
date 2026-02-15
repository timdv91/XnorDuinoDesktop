from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.models.address import XBee64BitAddress

class WallLightZigbeeAPI():
    def __init__(self, pRemoteMAC, pLocalPort, pBaut = 9600):
        self.XBEE = XBeeDevice(pLocalPort, pBaut)
        self.XBEE.open()
        self.REMOTE_DEV = RemoteXBeeDevice(self.XBEE, XBee64BitAddress.from_hex_string(pRemoteMAC))


    def _triggerLightSSRelay_Off(self):                                                                                     # Trigers the actual relay
        self.REMOTE_DEV.set_dio_value(IOLine.DIO12, IOValue.LOW)

    def _triggerLightSSRelay_On(self):                                                                                     # Trigers the actual relay
        self.REMOTE_DEV.set_dio_value(IOLine.DIO12, IOValue.HIGH)

    def setDimValue_WW(self, pVal):
        self.REMOTE_DEV.set_pwm_duty_cycle(IOLine.DIO10_PWM0, pVal)

    def setDimValue_CW(self, pVal):
        self.REMOTE_DEV.set_pwm_duty_cycle(IOLine.DIO11_PWM1, pVal)


    def saveNewConfig(self):
        self.REMOTE_DEV.set_parameter(b'WR', b'')

# Initialize object:
CZ_API = WallLightZigbeeAPI("0013A20041BD107F","/dev/ttyUSB0")

#CZ_API._triggerLightSSRelay_Off()
CZ_API.setDimValue_WW(100) # must be 0x19E or 414 pwm value
CZ_API.setDimValue_CW(100) # must be 0x60 or 96 pwm value
#CZ_API.saveNewConfig()
