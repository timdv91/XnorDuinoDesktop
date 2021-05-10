from FlaskGUI.API.xnorbusWebrequestor import xnorbusWebrequestor
from FlaskGUI.API.xnorbusRequestorHelper import xnorbusRequestorHelper
from flask import Flask, render_template
from flask import request

XRQ = xnorbusWebrequestor('http://127.0.0.1:8080')
XRH = xnorbusRequestorHelper(XRQ)

app = Flask(__name__)

# Page that shows index.html, this page inherits content from the base.html file:
@app.route('/')
def index():
    devIdList = XRH.initDeviceIDScan()
    devicesDictionary = XRH.getDevicesInfoDict(devIdList, pDebug=True)
    print(devicesDictionary)

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

    return render_template('index.html', posts=devicesDictionary)

# a simple hello world text:
@app.route('/devices', methods=('GET', 'POST'))
def devices():
    print("HELLO")
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