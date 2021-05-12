from FlaskGUI.API.xnorbusWebrequestor import xnorbusWebrequestor
from FlaskGUI.API.xnorbusRequestorHelper import xnorbusRequestorHelper
from flask import Flask, render_template
from flask import request
import atexit, threading
from flask_socketio import SocketIO, emit, send
import json, os
import time

XRQ = xnorbusWebrequestor('http://127.0.0.1:8080')
XRH = xnorbusRequestorHelper(XRQ)

# =========================================================
# Delay between device list refreshes: (in sec)
POOL_TIME = 5

# variables that are accessible from anywhere
commonDataStruct = {}

# lock to control access to variable
dataLock = threading.Lock()

# thread handler
THREAD_refreshDeviceList = None

# check the serial load on serial port
autoRefreshDevList_LockEpoch = 0
autoRefreshDevList_LockDuration = 5
autoRefreshDevList_isLocked = False
# =========================================================

def create_app():
    app = Flask(__name__)

    # ======================================================================================================
    socketio = SocketIO(app)

    @socketio.on('heart_beat')
    def subGUI_HeartBeat():
        global autoRefreshDevList_LockEpoch
        autoRefreshDevList_LockEpoch = int(time.time()) + autoRefreshDevList_LockDuration
        global autoRefreshDevList_isLocked
        emit('isLocked', autoRefreshDevList_isLocked)

    @socketio.on('connect')
    def subGUI_connected():
        global autoRefreshDevList_LockEpoch
        global autoRefreshDevList_LockDuration
        autoRefreshDevList_LockEpoch = int(time.time()) + autoRefreshDevList_LockDuration

    @socketio.on('get_value')
    def get_value(data):
        rcvBytes = XRQ.get(str(data['cmd']), "RS")  # set de master for ReadSlave
        if(rcvBytes != None):
            rcvBytes = eval(rcvBytes)
            rcvList = []
            for i in range(0,len(rcvBytes)):
                rcvList.append(rcvBytes[i])
            emit('value_reply', {"name":data['name'], "value": rcvList})

    # ======================================================================================================


    # Page that shows index.html, this page inherits content from the base.html file:
    @app.route("/")
    def index():
        global commonDataStruct
        devicesDictionary = commonDataStruct

        return render_template('index.html', posts=devicesDictionary)


    # a simple hello world text:
    @app.route('/devices', methods=('GET', 'POST'))
    def devices():
        devicePage = None
        I2C_ID = None
        if request.method == 'GET':
            devicePage = request.args['DEV_PAGE']
            I2C_ID = request.args['I2C_ID']

        return render_template(devicePage, posts=I2C_ID)


    # Rerouting for the about button:
    @app.route('/about')
    def about():
        return render_template('about.html')

    return app


#=======================================================================================================
class create_thread():
    def __init__(self):
        print("Starting thread creation")
        # Do initialisation stuff here
        # Create your thread
        global POOL_TIME
        global THREAD_refreshDeviceList

        THREAD_refreshDeviceList = threading.Timer(POOL_TIME, self.doStuff)
        THREAD_refreshDeviceList.start()

    def __del__(self):
        atexit.register(self.interrupt)

    def interrupt(self):
        global THREAD_refreshDeviceList
        print("Thread is being destroyed")
        try:
            THREAD_refreshDeviceList.cancel()
        except Exception:
            None

    def doStuff(self):
        global commonDataStruct
        global THREAD_refreshDeviceList
        global autoRefreshDevList_LockEpoch
        global autoRefreshDevList_isLocked
        with dataLock:
        # Do your stuff with commonDataStruct Here
            print("Thread started: ", threading.get_ident())

            if autoRefreshDevList_LockEpoch < int(time.time()):
                print("Hardware communication: Started")
                autoRefreshDevList_isLocked = False
                devIdList = XRH.initDeviceIDScan()
                devicesDictionary = XRH.getDevicesInfoDict(devIdList, pDebug=False)
                devicesDictionaryNested = XRH.getDevicesNestingDict(devicesDictionary, pDebug=False)
                print("Hardware communication: Completed")

                commonDataStruct = devicesDictionaryNested
            else:
                print("Hardware communication: Locked")
                autoRefreshDevList_isLocked = True

            print("Thread ended: ", threading.get_ident())
            # Set the next thread to happen
            THREAD_refreshDeviceList = threading.Timer(POOL_TIME, self.doStuff)
            THREAD_refreshDeviceList.start()

#=======================================================================================================


app = create_app()
#app.env = 'development'

if(app.env == 'development'):
    app.debug = True
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/API/scannedDevicesDict.json') as f:
        commonDataStruct = json.load(f)
else:
    create_thread()

app.run(host='0.0.0.0', port=5000)





