from flask import Flask, render_template
from flask import request
app = Flask(__name__)


# a simple hello world text:
@app.route('/hello')
def hello_world():
    return 'Hello, World!!'

# simple page showing indexOld.html file from /templates that uses some css from static/css:
@app.route('/indexOld')
def indexOld():
    return render_template('indexOld.html')

# Page that shows index.html, this page inherits content from the __devicesBase__.html file:
@app.route('/')
def index():
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
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        print(title)
        print(content)

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

    return render_template('configure.html')

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