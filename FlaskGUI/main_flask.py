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
    devInfoDict = XRH.getDevicesInfoDict(devIdList)

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
    return render_template('index.html', posts=posts)

# a simple hello world text:
@app.route('/device', methods=('GET', 'POST'))
def device():
    if request.method == 'GET':
        id = request.args['id']


        print(id)

        '''
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        '''

    return render_template("/devices/" + id + ".html")


# Rerouting for the about button:
@app.route('/about')
def about():
    return render_template('about.html')