import time

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.models.address import XBee64BitAddress

class KitchenLightsZigbeeAPI():
    def __init__(self, pRemoteMAC, pLocalPort, pBaut = 9600):
        self.LIGHT_INTENSITY = 100
        self.LIGHT_TEMPERATURE = 100

        xbee = XBeeDevice(pLocalPort, pBaut)
        xbee.open()
        self.REMOTE_DEV = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string(pRemoteMAC))

    def getLightOnState(self):
        value = self.REMOTE_DEV.get_io_configuration(IOLine.DIO12)
        if value == IOMode.DIGITAL_OUT_HIGH:
            return True
        else:
            return False

    def getLightTemperatureState(self):
        value_pwm0 = self.REMOTE_DEV.get_pwm_duty_cycle(IOLine.DIO10_PWM0)
        value_pwm1 = self.REMOTE_DEV.get_pwm_duty_cycle(IOLine.DIO11_PWM1)
        return value_pwm0, value_pwm1

    def setLightIntensity(self, pValue):
        if pValue > 100:
            pValue = 100
        if pValue < 10:
            pValue = 10

        self.LIGHT_INTENSITY = pValue
        pwm0, pwm1 = self.getLightTemperatureState()
        self.setLightTemperatureState(pwm0)

    def setLightTemperatureState(self, pValue):
        if pValue > 100:
            pValue = 100
        if pValue < 0:
            pValue = 0
        self.LIGHT_TEMPERATURE = pValue

    def setConfigApply(self):
        self.REMOTE_DEV.set_pwm_duty_cycle(IOLine.DIO10_PWM0, int(self.LIGHT_TEMPERATURE*(self.LIGHT_INTENSITY/100)))
        self.REMOTE_DEV.set_pwm_duty_cycle(IOLine.DIO11_PWM1, int((100-self.LIGHT_TEMPERATURE)*(self.LIGHT_INTENSITY/100)))

# Initialize object:
KL_API = KitchenLightsZigbeeAPI("0013A20041BD1002","/dev/ttyUSB2")

ligtsOn = KL_API.getLightOnState()
print("The lights are on: " + str(ligtsOn))
pwm = KL_API.getLightTemperatureState()
print(pwm)

KL_API.setLightIntensity(90)
KL_API.setLightTemperatureState(75)
KL_API.setConfigApply()

pwm = KL_API.getLightTemperatureState()
print(pwm)