from FlaskGUI.API.xnorbusWebrequestor import xnorbusWebrequestor
from FlaskGUI.API.xnorbusRequestorHelper import xnorbusRequestorHelper
from flask import Flask, render_template
from flask import request
import atexit, threading
from flask_socketio import SocketIO, join_room, leave_room
import os


XRQ = xnorbusWebrequestor('http://127.0.0.1:8080')
XRH = xnorbusRequestorHelper(XRQ)

# =========================================================
POOL_TIME = 5
# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = None
# =========================================================

def create_app():
    app = Flask(__name__)

    # ======================================================================================================
    socketio = SocketIO(app)

    @socketio.on('connect')
    def test_connect():
        print("client connected")

    # ======================================================================================================

    # Page that shows deviceList.html, this page inherits content from the __devicesBase__.html file:
    @app.route("/")
    def index():
        global commonDataStruct
        devicesDictionary = commonDataStruct

        return render_template('deviceList.html', posts=devicesDictionary)

    # a simple hello world text:
    @app.route('/devices', methods=('GET', 'POST'))
    def devices():
        global yourThread
        print(threading.active_count())

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
        global yourThread
        global POOL_TIME

        print("ThreadCount", threading.active_count())
        yourThread = threading.Timer(POOL_TIME, self.doStuff)
        yourThread.start()

    def __del__(self):
        atexit.register(self.interrupt())

    def interrupt(self):
        global yourThread
        print("Thread is being destroyed")
        try:
            yourThread.cancel()
        except Exception:
            None

    def doStuff(self):
        global commonDataStruct
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
            print("Thread started: ", threading.get_ident())

            devIdList = XRH.initDeviceIDScan()
            devicesDictionary = XRH.getDevicesInfoDict(devIdList, pDebug=True)
            devicesDictionaryNested = XRH.getDevicesNestingDict(devicesDictionary, pDebug=True)

            commonDataStruct = devicesDictionaryNested

            print("Thread ended: ", threading.get_ident())
            # Set the next thread to happen
            yourThread = threading.Timer(POOL_TIME, self.doStuff)
            yourThread.start()


#=======================================================================================================




app = create_app()

if(app.env == "development"):
    print(threading.active_count())
    if(threading.active_count() <= 2):
        create_thread()
else:
    create_thread()



