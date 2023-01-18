from SRC.GUI.ThreadedBackgroundWorker import ThreadedBackgroundWorker
from SRC.GUI.FrontEndDataHandler import DeviceListLoader, TreeViewLoader, DevicesPageLoader, DevicesPageWriter
from SRC.HardWare.xnorbusWebrequestor import xnorbusWebrequestor
from SRC.GUI.xnorbusRequestorHelper import xnorbusRequestorHelper
from SRC.DAQ.xnorbusDAQ import xnorbusDAQ
from SRC.TMP.temporaryFileManager import temporaryFileManager
from SRC.GUI.IP import IP

from flask import Flask, render_template
from flask import request
import threading
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
HOST_PORT = 5000

# =========================================================
# variables that are accessible from anywhere
class GlobVars():
    POOL_TIME = 10  # Delay between device list (thread) refreshes: (in sec)                                            --> Use on 10Khz I2C clock
    #POOL_TIME = 5  # Delay between device list (thread) refreshes: (in sec)                                            --> Use on 100Khz I2C clock
    commonDataStruct = {}  # global struct that stores the deviceList parameters
    dataLock = threading.Lock()  # lock to control access to variable

    THREAD_refreshDeviceList = None  # thread handler
    currentlyOpenedMainPage = None  # keeps track of the currently opened webpage
    runThreadOnLoadedPages = ['treeView', 'deviceList']  # run communication thread when one of these pages are opened

    # check the serial load on serial port
    autoRefreshDevList_LockEpoch = 0  # contains the epoch when autorefresh of deviceList gets paused.
    autoRefreshDevList_LockDuration = 8  # contains the amount of seconds autorefresh lists should stay paused          --> Use on 10Khz I2C clock
    #autoRefreshDevList_LockDuration = 3  # contains the amount of seconds autorefresh lists should stay paused         --> Use on 100Khz I2C clock
    autoRefreshDevList_isLocked = True  # if True deviceList will extend pause state with <lockdurations> seconds
    # =========================================================
globVars = GlobVars()


def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    # ============================ DeviceList and TreeView socketIO requests: ==============================
    # ======================================================================================================
    # individual device pages send a heartbeat each N'th second to keep the autorefresh state paused.
    @socketio.on('heart_beat')
    def subGUI_HeartBeat():
        globVars.autoRefreshDevList_LockEpoch = int(time.time()) + globVars.autoRefreshDevList_LockDuration
        emit('isLocked', globVars.autoRefreshDevList_isLocked)

    # individual devices pages emit 'connect' when they are opened to set autorefresh state to paused.
    @socketio.on('connect')
    def subGUI_connected():
        globVars.autoRefreshDevList_LockEpoch = int(time.time()) + globVars.autoRefreshDevList_LockDuration

    # individual devices pages communication route to read slave devices.
    @socketio.on('get_value')
    def get_value(data):
        rcvBytes, commErrorCount = XRQ.get(str(data['cmd']), str(data['cmdType']))  # set de master for ReadSlave
        if(rcvBytes != None):
            rcvBytes = eval(rcvBytes)
            rcvList = []
            for i in range(0, len(rcvBytes)):
                rcvList.append(rcvBytes[i])
            emit('value_reply', {"name":data['name'], "value": rcvList})

    @socketio.on('clearDevList')
    def clearDevList():
        globVars.commonDataStruct = {}

    # ============================ Main page and About page Get and Post requests: =========================
    # ======================================================================================================

    # Rerouting for the index page:
    @app.route('/')
    def index():
        globVars.currentlyOpenedMainPage = 'index'
        return render_template('index.html')

    # Rerouting for the about button:
    @app.route('/about')
    def about():
        globVars.currentlyOpenedMainPage = 'about'
        return render_template('about.html')

    # ============================ DAQ page Get and Post requests: =========================
    # ======================================================================================================

    # Rerouting for the about button:
    @app.route('/dataAcquisition')
    def dataAcquisition():                                                      #TODO: CLEAN UP THIS MESS!
        globVars.currentlyOpenedMainPage = 'dataAcquisition'
        if(len(globVars.commonDataStruct) <= 0):
            globVars.commonDataStruct = TFM.readDevListFromFile()
        DAQConfig = XDAQ.readConfigFromFile()
        return render_template('dataAcquisition.html', posts=DAQConfig, devices=globVars.commonDataStruct)

    # Rerouting for the about button:
    @app.route('/dataAcquisition_write')
    def dataAcquisition_write():                                                #TODO: CLEAN UP THIS MESS!
        globVars.currentlyOpenedMainPage = 'dataAcquisition'

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
        return render_template('dataAcquisition.html', posts=DAQConfig, devices=globVars.commonDataStruct)

    # ============================ DeviceList and TreeView Get and Post requests: ==============================
    # ======================================================================================================

    # Page that shows deviceList.html, this page inherits content from the __base__.html file:
    @app.route("/deviceList")
    def deviceList():
        globVars.currentlyOpenedMainPage = 'deviceList'
        devicesDictionary = copy.deepcopy(globVars.commonDataStruct)

        DLL = DeviceListLoader()
        devicesDictionary = DLL.dictKeyErrorCheck(devicesDictionary)

        devicesDictionary['AUTO_UPDATE_LOCKED'] = globVars.autoRefreshDevList_isLocked
        return render_template('deviceList.html', posts=devicesDictionary)

    # Page that shows treeView.html, this page inherits content from the __base__.html file:
    @app.route('/treeView')
    def treeView():
        globVars.currentlyOpenedMainPage = 'treeView'
        devicesDictionary = copy.deepcopy(globVars.commonDataStruct)

        TVL = TreeViewLoader()
        devicesDictionary = TVL.dictKeyErrorCheck(devicesDictionary)
        devicesDictionary = TVL.nestedDictParameterCleanup(devicesDictionary)
        devicesDictionary = TVL.addingNewNestedParameters(devicesDictionary)
        devicesDictionary = TVL.retagPreviouslyNestedDevices(devicesDictionary)

        devicesDictionary['AUTO_UPDATE_LOCKED'] = globVars.autoRefreshDevList_isLocked
        return render_template('treeView.html', posts=devicesDictionary)

    # ============================ Device page Get and Post requests: ======================================
    # ======================================================================================================

    # Page that shows individual device pages, inherits content from the __devicesBase__.html file:
    @app.route('/devices', methods=('GET', 'POST'))
    def devices():
        DPL = DevicesPageLoader(request)
        posts = DPL.dataLoader()

        return render_template(posts['DEV_PAGE'], posts=posts, title=posts['DEV_TYPE'], hostIP=HOST_IP+":"+str(HOST_PORT))

    # individual devices pages communication route to write slave devices.
    @app.route('/devices_write')
    def devices_write():
        DPW = DevicesPageWriter(request)
        posts, send_startId, send_n = DPW.getRequestData()
        sendValue, isValid = DPW.getErrorCheck(send_n)
        cmd, writeMethod = DPW.getWriteCommand(posts, send_startId, send_n, sendValue)
        DPW.executeWriteCommand(XRQ, cmd, writeMethod, isValid)

        return render_template(posts['DEV_PAGE'], title=posts['DEV_TYPE'], posts=posts, inputIsValid=isValid, hostIP=HOST_IP+":"+str(HOST_PORT))

    return app

# ========================================== Flask launcher: ===========================================
# ======================================================================================================
app = create_app()
#app.env = 'development'

if(app.env == 'development'):
    app.debug = True
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/DB/TMP/tmpDeviceList.json') as f:
        globVars.commonDataStruct['SLAVES'] = json.load(f)
else:
    ThreadedBackgroundWorker(globVars, XRH, XDAQ, TFM)

app.run(host=HOST_IP, port=HOST_PORT) # set HOST_IP and HOST_PORT on top of this page!