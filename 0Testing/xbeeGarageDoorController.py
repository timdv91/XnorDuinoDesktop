import time

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.models.address import XBee64BitAddress

class CarportZigbeeAPI():
    def __init__(self, pRemoteMAC, pLocalPort, pBaut = 9600):
        xbee = XBeeDevice(pLocalPort, pBaut)
        xbee.open()
        self.REMOTE_DEV = RemoteXBeeDevice(xbee, XBee64BitAddress.from_hex_string(pRemoteMAC))
        # Configure the DIO2_AD2 line of the local device to be Digital input.
        self.REMOTE_DEV.set_io_configuration(IOLine.DIO2_AD2, IOMode.DIGITAL_IN)
        # Configure the DIO1_AD1 line of the local device to be Digital output (set high by default).
        self.REMOTE_DEV.set_io_configuration(IOLine.DIO3_AD3, IOMode.DIGITAL_OUT_LOW)

    def _triggerCarportRelay(self):                                                                                     # Trigers the actual relay
        # Pulse carport open/close:
        self.REMOTE_DEV.set_dio_value(IOLine.DIO3_AD3, IOValue.HIGH)
        time.sleep(2)
        self.REMOTE_DEV.set_dio_value(IOLine.DIO3_AD3, IOValue.LOW)

    def waitOnCarportFeedback(self, pStartingClosedState, pWaitForSeconds = 10):                                        # Waits 'n' seconds until the carport reaches it's new state.
        for i in range(0, pWaitForSeconds):
            currentClosedState = self.getCarportStateClosed()
            if currentClosedState != pStartingClosedState:
                return True
            time.sleep(1)
        return False

    def getCarportStateClosed(self):                                                                                    # Returns true if the carport is closed, false if open
        value = self.REMOTE_DEV.get_dio_value(IOLine.DIO2_AD2)
        if value == IOValue.HIGH:
            return True
        else:
            return False

    def setCarportOpen(self):                                                                                           # Triggers the switch relay, but only when carport was closed
        if self.getCarportStateClosed() == True:
            self._triggerCarportRelay()
            return True
        return False

    def setCarportClosed(self):                                                                                         # Triggers the switch relay, but only when carport was open
        if self.getCarportStateClosed() == False:
            self._triggerCarportRelay()
            return True
        return False


# Initialize object:
CZ_API = CarportZigbeeAPI("0013A20041A8824F","/dev/ttyUSB2")

# Get current carport closed state:
carportIsClosed = CZ_API.getCarportStateClosed()
print("The carport is currently closed: " + str(carportIsClosed))

# Trigger the carport either open or closed:
if carportIsClosed == True:
    print("Sending open command to carport: ", end="")
    if CZ_API.setCarportOpen() == True:
        print("Success!")
else:
    print("Sending closed command to carport: ", end="")
    if CZ_API.setCarportClosed() == True:
        print("Success!")

# Wait for carport to respond with successful execution of command:
print("Carport responded to command: ", end="")
fb = CZ_API.waitOnCarportFeedback(carportIsClosed)
print(fb)