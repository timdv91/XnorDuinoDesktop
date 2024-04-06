from SRC.GUI.DeviceScan import DeviceScan                                   # Can be ignored if this import causes an error, needs to be like this to function outside IDE.
import atexit, threading                                                    # TODO: Find out why above line causes error in IDE, but has to be like to function outside IDE.
import time

class ThreadedBackgroundWorker():
    # Create new thread to run background tasks asynchronously:
    def __init__(self, pGlobVars, pXRH):
        self.globVars = pGlobVars
        self.XRH = pXRH

        print("Starting thread creation")
        # Create your thread
        self.globVars.THREAD_refreshDeviceList = threading.Timer(self.globVars.POOL_TIME, self.doStuff)
        self.globVars.THREAD_refreshDeviceList.start()

    # Call backgroundworkers assassin for deletion of the child thread (should happen automatically)
    def __del__(self):
        atexit.register(self.interrupt)

    # the interrupt that actually kills the backgroundworker:
    def interrupt(self):
        print("Thread is being destroyed")
        try:
            self.globVars.THREAD_refreshDeviceList.cancel()
        except Exception:
            None

    # the backgroundworker:
    def doStuff(self):
        with self.globVars.dataLock:
        # Do your stuff with commonDataStruct Here
            print("Thread started: ", threading.get_ident())
            if(self.globVars.currentlyOpenedMainPage in self.globVars.runThreadOnLoadedPages):          # prevent loading deviceList when page is not loaded
                self.globVars.currentlyOpenedMainPage = None                                            # clear the currentlyOpenedMainPage to prevent auto updates after page is closed!
                self.runBusDeviceScan()                                                                 # On each refresh of the page this value is restored automatically for next update.
            else:
                None                                                                                    # Here we can execute stuff, whenever the GUI is inactive.

            print("Thread ended: ", threading.get_ident())
            # Set the next thread to happen
            self.globVars.THREAD_refreshDeviceList = threading.Timer(self.globVars.POOL_TIME, self.doStuff)
            self.globVars.THREAD_refreshDeviceList.start()

    # do device scan on separated thread:
    def runBusDeviceScan(self):
        try:
            if self.globVars.autoRefreshDevList_LockEpoch < int(time.time()):  # prevent loading deviceList when device is opened
                self.globVars.autoRefreshDevList_isLocked = False

                DS = DeviceScan(self.XRH)
                self.globVars.commonDataStruct = DS.getMasterInfo(self.globVars.commonDataStruct)

                try:
                    devIdList = DS.getMasterSlavesIdList(self.globVars.commonDataStruct)
                    devDictionary = DS.getSlavesInfo(devIdList)
                    self.globVars.commonDataStruct = DS.getNestingChildDevices(self.globVars.commonDataStruct, devDictionary)

                    if(DS.getErrorStats() > 0):
                        print("Communication error detected, ignoring potentially corrupted data!")

                except KeyError as e:
                    print(str(e))

                print("Hardware communication: Completed")
            else:
                print("Hardware communication: Locked")
                self.globVars.autoRefreshDevList_isLocked = True
        except TypeError as e:
            print(str(e))
