from SRC.xnorbusWebrequestor import xnorbusWebrequestor
from SRC.GUI.xnorbusRequestorHelper import xnorbusRequestorHelper
from SRC.DAQ.xnorbusDAQ import xnorbusDAQ
from SRC.TMP.temporaryFileManager import temporaryFileManager
from SRC.GUI.IP import IP

'''
from FlaskGUI.SRC.xnorbusWebrequestor import xnorbusWebrequestor
from FlaskGUI.SRC.GUI.xnorbusRequestorHelper import xnorbusRequestorHelper
from FlaskGUI.SRC.DAQ.xnorbusDAQ import xnorbusDAQ
from FlaskGUI.SRC.TMP.temporaryFileManager import temporaryFileManager
'''

from flask import Flask, render_template
from flask import request
import atexit, threading
from flask_socketio import SocketIO, emit
import json, os
import time
import copy

#XRQ = xnorbusWebrequestor('http://192.168.1.65:8080')
#XRQ = xnorbusWebrequestor('http://192.168.1.28:8080')
XRQ = xnorbusWebrequestor('http://127.0.0.1:8080')

XRH = xnorbusRequestorHelper(XRQ, "DEVconfig.json")
XDAQ = xnorbusDAQ(XRQ, "DAQconfig.json")
TFM = temporaryFileManager("tmpDeviceList.json")

HOST_IP = IP().get_ip()
#HOST_IP = '127.0.0.1'
#HOST_IP = '192.168.1.65'
HOST_PORT = 5000

# =========================================================
# variables that are accessible from anywhere
POOL_TIME = 5                               # Delay between device list (thread) refreshes: (in sec)
commonDataStruct = {}                       # global struct that stores the deviceList parameters
dataLock = threading.Lock()                 # lock to control access to variable

THREAD_refreshDeviceList = None                         # thread handler
currentlyOpenedMainPage = None                          # keeps track of the currently opened webpage
runThreadOnLoadedPages = ['treeView', 'deviceList']     # run communication thread when one of these pages are opened

# check the serial load on serial port
autoRefreshDevList_LockEpoch = 0            # contains the epoch when autorefresh of deviceList gets paused.
autoRefreshDevList_LockDuration = 3         # contains the amount of seconds autorefresh lists should stay paused
autoRefreshDevList_isLocked = True          # if True deviceList will extend pause state with <lockdurations> seconds
# =========================================================

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    # ============================ DeviceList and TreeView socketIO requests: ==============================
    # ======================================================================================================
    # individual device pages send a heartbeat each N'th second to keep the autorefresh state paused.
    @socketio.on('heart_beat')
    def subGUI_HeartBeat():
        global autoRefreshDevList_LockEpoch
        autoRefreshDevList_LockEpoch = int(time.time()) + autoRefreshDevList_LockDuration
        global autoRefreshDevList_isLocked
        emit('isLocked', autoRefreshDevList_isLocked)

    # individual devices pages emit 'connect' when they are opened to set autorefresh state to paused.
    @socketio.on('connect')
    def subGUI_connected():
        global autoRefreshDevList_LockEpoch
        global autoRefreshDevList_LockDuration
        autoRefreshDevList_LockEpoch = int(time.time()) + autoRefreshDevList_LockDuration

    # individual devices pages communication route to read slave devices.
    @socketio.on('get_value')
    def get_value(data):
        rcvBytes = XRQ.get(str(data['cmd']), str(data['cmdType']))  # set de master for ReadSlave
        if(rcvBytes != None):
            rcvBytes = eval(rcvBytes[0])

            rcvList = []
            for i in range(0,len(rcvBytes)):
                rcvList.append(rcvBytes[i])
            emit('value_reply', {"name":data['name'], "value": rcvList})

    @socketio.on('clearDevList')
    def clearDevList():
        global commonDataStruct
        commonDataStruct = {}

    # ============================ Main page and About page Get and Post requests: =========================
    # ======================================================================================================

    # Rerouting for the index page:
    @app.route('/')
    def index():
        global currentlyOpenedMainPage
        currentlyOpenedMainPage = 'index'
        return render_template('index.html')

    # Rerouting for the about button:
    @app.route('/about')
    def about():
        global currentlyOpenedMainPage
        currentlyOpenedMainPage = 'about'
        return render_template('about.html')

    # ============================ DAQ page Get and Post requests: =========================
    # ======================================================================================================

    # Rerouting for the about button:
    @app.route('/dataAcquisition')
    def dataAcquisition():
        global currentlyOpenedMainPage
        global commonDataStruct
        currentlyOpenedMainPage = 'dataAcquisition'

        if(len(commonDataStruct) <= 0):
            commonDataStruct = TFM.readDevListFromFile()

        DAQConfig = XDAQ.readConfigFromFile()
        return render_template('dataAcquisition.html', posts=DAQConfig, devices=commonDataStruct)

    # Rerouting for the about button:
    @app.route('/dataAcquisition_write')
    def dataAcquisition_write():
        global currentlyOpenedMainPage
        global commonDataStruct
        currentlyOpenedMainPage = 'dataAcquisition'

        if request.method == 'GET':
            DAQConfig = eval(request.args.getlist('posts')[0])  # Why inside an array? Check this later on?

            if(request.args['cmd'] == "config"):
                DAQConfig['DATABASE']['URL'] = request.args['ServerIP']
                DAQConfig['DATABASE']['PORT'] = request.args['ServerPort']
                DAQConfig['DATABASE']['USER'] = request.args['DatabaseUser']
                DAQConfig['DATABASE']['PASS'] = request.args['DatabasePass']

                # Fix the nonsensical crap an HTML checkbox brings with it:
                checkBoxState = None
                try:
                    checkBoxState = request.args['DatabaseEncrypted']
                    if(checkBoxState != False):
                        checkBoxState = True
                except:
                    checkBoxState = False

                DAQConfig['DATABASE']['ENCRYPTION'] = checkBoxState

            elif(request.args['cmd'] == "DAQSettings"):
                print("Add daq rules here to daqConfig file")
            else:
                print("ERROR: '/dataAcquisition_write' - Unknown option")

            XDAQ.writeConfigToFile(DAQConfig)
        return render_template('dataAcquisition.html', posts=DAQConfig, devices=commonDataStruct)

    # ============================ DeviceList and TreeView Get and Post requests: ==============================
    # ======================================================================================================

    # Page that shows deviceList.html, this page inherits content from the __base__.html file:
    @app.route("/deviceList")
    def deviceList():
        global commonDataStruct
        global autoRefreshDevList_isLocked
        global currentlyOpenedMainPage
        currentlyOpenedMainPage = 'deviceList'

        devicesDictionary = copy.deepcopy(commonDataStruct)
        try:
            t = devicesDictionary['SLAVES']
            t = devicesDictionary['MASTER']
        except KeyError:
            devicesDictionary['SLAVES'] = {}
            devicesDictionary['MASTER'] = {}
        devicesDictionary['AUTO_UPDATE_LOCKED'] = autoRefreshDevList_isLocked

        return render_template('deviceList.html', posts=devicesDictionary)

    # Rerouting for the about button:
    @app.route('/treeView')
    def treeView():
        global commonDataStruct
        global autoRefreshDevList_isLocked
        global currentlyOpenedMainPage
        currentlyOpenedMainPage = 'treeView'

        devicesDictionary = copy.deepcopy(commonDataStruct)
        try:
            t = devicesDictionary['SLAVES']
            t= devicesDictionary['MASTER']
        except KeyError:
            devicesDictionary['SLAVES'] = {}
            devicesDictionary['MASTER'] = {}

        devicesDictionary['AUTO_UPDATE_LOCKED'] = autoRefreshDevList_isLocked

        # Clearing ugly parameters from Nested dictionary var:
        for i in range(0, len(devicesDictionary['SLAVES'])):
            if(str(type(devicesDictionary['SLAVES'][i]['NESTED'])) != "<class 'list'>"):
                devicesDictionary['SLAVES'][i]['NESTED'] = ""

        # adding a new parameter to dictionary var, to determine if the device has already been listed as nested device:
        for i in range(0, len(devicesDictionary['SLAVES'])):
           devicesDictionary['SLAVES'][i]['isNested'] = False  # set each device as not nested in list

        # check what devices have previously been listed as nested devices, tag them:
        for i in range(0, len(devicesDictionary['SLAVES'])):
            for o in range(0,len(devicesDictionary['SLAVES'][i]['NESTED'])):
                #print(devicesDictionary['SLAVES'][i]['NESTED'][o])
                for p in range(0,len(devicesDictionary['SLAVES'])):
                    #print("\t", devicesDictionary['SLAVES'][p]['I2C_ID'], end=" ")
                    if(int(devicesDictionary['SLAVES'][i]['NESTED'][o]) == int(devicesDictionary['SLAVES'][p]['I2C_ID'])):
                        devicesDictionary['SLAVES'][p]['isNested'] = True  # set specific devices as listed in list
                        #print("- detected")
                        break
                    #print()

        return render_template('treeView.html', posts=devicesDictionary)

    # ============================ Device page Get and Post requests: ======================================
    # ======================================================================================================

    # Page that shows individual device pages, inherits content from the __devicesBase__.html file:
    @app.route('/devices', methods=('GET', 'POST'))
    def devices():
        DEV_PAGE = None
        DEV_TYPE = None
        posts = {}
        if request.method == 'GET':
            DEV_PAGE = request.args['DEV_PAGE']
            DEV_TYPE = request.args['DEV_TYPE']
            posts['DEV_TYPE'] = request.args['DEV_TYPE']
            posts['DEV_PAGE'] = request.args['DEV_PAGE']
            posts['I2C_ID'] = request.args['I2C_ID']
            posts['HW_ID'] = request.args['HW_ID']
            posts['FW_ID'] = request.args['FW_ID']

        return render_template(DEV_PAGE, posts=posts, title=DEV_TYPE, hostIP=HOST_IP+":"+str(HOST_PORT))

    # individual devices pages communication route to write slave devices.
    @app.route('/devices_write')
    def devices_write():
        DEV_TYPE = None
        DEV_PAGE = None
        posts = None
        isValid = True
        if request.method == 'GET':
            posts = eval(request.args.getlist('posts')[0])  # Why inside an array? Check this later on?

            DEV_TYPE = posts['DEV_TYPE']
            DEV_PAGE = posts['DEV_PAGE']
            I2C_ID = posts['I2C_ID']
            send_startId = eval(request.args.getlist('cmd')[0])[0]
            send_n = eval(request.args.getlist('cmd')[0])[1]

            sendValue = ""
            for i in range(0, send_n):
                nr = request.args.getlist(str(i))[0]
                sendValue += ", " + str(nr)
                try:
                    if int(nr) < 0 or int(nr) > 255:
                        isValid = False
                except ValueError:
                    isValid = False

            writeMethod = None
            if(I2C_ID != '0'):
                cmd = "[" + str(I2C_ID) + ", " + str(send_startId) + ", " + str(send_n) + "" + str(sendValue) + "]"
                writeMethod = 'WS'
            else:
                cmd = "[" + str(send_startId) + ", " + str(send_n) + "" + str(sendValue) + "]"
                writeMethod = 'WM'
            print(cmd)                                     # last comma is automatically put in place!

            if isValid:
                print("Valid input!",  writeMethod)
                rcvBytes = XRQ.get(str(cmd), writeMethod)[0]  # set de master for ReadSlave
                print(rcvBytes)
            else:
                print("Invalid input!")

        return render_template(DEV_PAGE, title=DEV_TYPE, posts=posts, inputIsValid=isValid, hostIP=HOST_IP+":"+str(HOST_PORT))

    return app

# ====================== MultiThreaded background worker for deviceScan and DAQ: =======================
# ======================================================================================================

class create_thread():
    # Create new thread to run background tasks asynchronously:
    def __init__(self):
        print("Starting thread creation")
        # Do initialisation stuff here
        # Create your thread
        global POOL_TIME
        global THREAD_refreshDeviceList

        THREAD_refreshDeviceList = threading.Timer(POOL_TIME, self.doStuff)
        THREAD_refreshDeviceList.start()

    # Call backgroundworkers assassin for deletion of the child thread (should happen automatically)
    def __del__(self):
        atexit.register(self.interrupt)

    # the interrupt that actually kills the backgroundworker:
    def interrupt(self):
        global THREAD_refreshDeviceList
        print("Thread is being destroyed")
        try:
            THREAD_refreshDeviceList.cancel()
        except Exception:
            None

    # the backgroundworker:
    def doStuff(self):
        global THREAD_refreshDeviceList
        global currentlyOpenedMainPage, runThreadOnLoadedPages
        with dataLock:
        # Do your stuff with commonDataStruct Here
            print("Thread started: ", threading.get_ident())
            if(currentlyOpenedMainPage in runThreadOnLoadedPages):          # prevent loading deviceList when page is not loaded
                currentlyOpenedMainPage = None                              # clear the currentlyOpenedMainPage to prevent auto updates after page is closed!
                self.runBusDeviceScan()                                     # On each refresh of the page this value is restored automatically for next update.
            else:
                self.runDAQ()                                               # When the XnorDuino configurator is not working, execute DAQ

            print("Thread ended: ", threading.get_ident())
            # Set the next thread to happen
            THREAD_refreshDeviceList = threading.Timer(POOL_TIME, self.doStuff)
            THREAD_refreshDeviceList.start()

    # do device scan on separated thread:
    def runBusDeviceScan(self):
        global commonDataStruct
        global autoRefreshDevList_LockEpoch
        global autoRefreshDevList_isLocked
        try:
            if autoRefreshDevList_LockEpoch < int(time.time()):  # prevent loading deviceList when device is opened
                autoRefreshDevList_isLocked = False

                print("Hardware communication: Started")
                commonDataStruct['MASTER'] = XRH.getMasterInformation()
                #print(commonDataStruct)
                devIdList = []

                try:
                    if(commonDataStruct['MASTER']['DEV_TYPE'] == 'Master'): # only scan for local slaves on a 'Master' module.
                        devIdList = XRH.initDeviceIDScan()

                    devicesDictionary = XRH.getDevicesInfoDict(devIdList, pDebug=False)
                    if(devicesDictionary != None):
                        commonDataStruct['SLAVES'] = XRH.getDevicesNestingDict(devicesDictionary['SLAVES'], pDebug=False)

                    TFM.writeDevListToFile(commonDataStruct) # write datastruct with devices to tmpFile
                except KeyError as e:
                    print(str(e))

                print("Hardware communication: Completed")
            else:
                print("Hardware communication: Locked")
                autoRefreshDevList_isLocked = True
        except TypeError as e:
            print(str(e))

    # do data acquisition on separated thread:
    def runDAQ(self):
        print("No configuration page opened, running DAQ execution...")
        print("Under construction...")
        #configData = XDAQ.readConfigFromFile()
        #print(configData['DATABASE'])



# ========================================== Flask launcher: ===========================================
# ======================================================================================================
app = create_app()
#app.env = 'development'

if(app.env == 'development'):
    app.debug = True
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/DB/TMP/tmpDeviceList.json') as f:
        commonDataStruct['SLAVES'] = json.load(f)
else:
    create_thread()

app.run(host=HOST_IP, port=HOST_PORT) # set HOST_IP and HOST_PORT on top of this page!





