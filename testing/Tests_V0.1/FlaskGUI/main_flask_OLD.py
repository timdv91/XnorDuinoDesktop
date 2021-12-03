from FlaskGUI.SRC.HardWare.xnorbusWebrequestor import xnorbusWebrequestor
from FlaskGUI.SRC.GUI.xnorbusRequestorHelper import xnorbusRequestorHelper
from flask import Flask, render_template
from flask import request
import atexit, threading


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
# Serial port lock:
SerialLock = False
# =========================================================

def create_app():
    app = Flask(__name__)

    # Page that shows deviceList.html, this page inherits content from the __devicesBase__.html file:
    @app.route("/")
    def index():
        global commonDataStruct
        devicesDictionary = commonDataStruct

        #devIdList = XRH.initDeviceIDScan()
        #devicesDictionary = XRH.getDevicesInfoDict(devIdList, pDebug=True)
        #devicesDictionaryNested = XRH.getDevicesNestingDict(devicesDictionary, pDebug=True)
        #print(devicesDictionaryNested)


        posts = []
        thisdict = {
            "title": "testTitle1",
            "created": "Mustang1",
            "id": "id=A"
        }
        posts.append(thisdict)
        thisdict = {
            "title": "testTitle2",
            "created": "Mustang2",
            "id": "id=Q"
        }
        posts.append(thisdict)

        return render_template('deviceList.html', posts=devicesDictionary)

    # a simple hello world text:
    @app.route('/devices', methods=('GET', 'POST'))
    def devices():
        print("HELLO2")
        if request.method == 'GET':
            devicePage = request.args['DEV_PAGE']
            I2C_ID = request.args['I2C_ID']

        print("Test1: ", devicePage)
        print("Test2: ", I2C_ID)

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

        #yourThread = threading.Thread(target=self.doStuff, args=())
        yourThread = threading.Timer(POOL_TIME, self.doStuff, ())
        yourThread.start()

    def __del__(self):
        atexit.register(self.interrupt())

    def interrupt(self):
        global yourThread
        print("Thread is being destroyed")
        yourThread.cancel()

    def doStuff(self):
        global commonDataStruct
        global yourThread
        global SerialLock
        with dataLock:
        # Do your stuff with commonDataStruct Here

            if SerialLock == True:
                return
            SerialLock = True

            print("Thread started: ", threading.get_ident())
            devIdList = XRH.initDeviceIDScan()
            devicesDictionary = XRH.getDevicesInfoDict(devIdList, pDebug=True)
            devicesDictionaryNested = XRH.getDevicesNestingDict(devicesDictionary, pDebug=True)
            print(devicesDictionaryNested)

            commonDataStruct = devicesDictionaryNested

            print("Thread ended: ", threading.get_ident())
            SerialLock = False

            # Set the next thread to happen
            yourThread = threading.Timer(POOL_TIME, self.doStuff, ())
            yourThread.start()

    #=======================================================================================================

app = create_app()
create_thread()