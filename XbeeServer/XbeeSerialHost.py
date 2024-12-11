from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.models.address import XBee64BitAddress

class XbeeSerialHost():
    def __init__(self, pPort, pBautrate=9600):
        self.PORT = pPort
        self.BAUT = pBautrate
        self.isConnectedHW = False


    def getHWConnectionState(self):
        return self.isConnectedHW

    def _connectionInit(self):
        try:
            self.XBEE = XBeeDevice(self.PORT, self.BAUT)
            self.XBEE.open()
            self.isConnectedHW = True
        except Exception as e:
            print(str(e))

    def _communication(self, pFunction, pData, pDebug=False):
        # Extract and log pData
        print("MAC:", pData[0])
        print("Function:", pData[1])
        print("Argument:", pData[2])

        # Instantiate the remote device
        REMOTE_DEV = RemoteXBeeDevice(self.XBEE, XBee64BitAddress.from_hex_string(pData[0]))

        retVal = True
        try:
            # Extract the function name
            func_name = pData[1].strip("()")  # Strip parentheses from function name

            # Resolve arguments
            resolved_args = []
            for arg in pData[2:]:
                try:
                    # Attempt to resolve constants like IOLine.DIO12 or IOMode.DIGITAL_OUT_LOW
                    resolved_arg = eval(arg, {"IOLine": IOLine, "IOMode": IOMode})
                except NameError:
                    # If it's not a known constant, assume it's a literal (e.g., "100")
                    resolved_arg = int(arg) if arg.isdigit() else arg
                resolved_args.append(resolved_arg)

            # Dynamically call the method on the REMOTE_DEV object
            if hasattr(REMOTE_DEV, func_name):
                func = getattr(REMOTE_DEV, func_name)
                if callable(func):
                    retVal = func(*resolved_args)  # Pass all resolved arguments
                    print("Result:", retVal)
                else:
                    raise ValueError(f"{func_name} is not callable.")
            else:
                raise AttributeError(f"{func_name} not found in REMOTE_DEV.")

            if pFunction == "/W" and retVal == None:
                return True
            else:
                return retVal
        except Exception as e:
            return False