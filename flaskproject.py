from flask import Flask,render_template,request,redirect,url_for,session
from workscrapper import workscrap
import os
from flask_socketio import SocketIO, _ManagedSession, emit
from time import sleep
from queue import Queue
import threading

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
app.secret_key = 'hello'
socketio = SocketIO(app)
q = Queue()

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'zejie123' or request.form['password'] != 'kong12345':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for(".index"))
    return render_template('login.html', error=error)

@app.route('/index',methods=['GET','POST'])
def index():
    session['workscrap_var'] = 0
    value = None
    if request.method == 'POST':
        if request.form['news'] == "workscrapper":
            value = os.listdir("D:\programming\python\webapp\static\job_pics")
    return render_template('index.html',value = value)

@app.route('/image/<img>',methods=['GET','POST'])
def image(img):
    if request.method == 'POST':
        os.remove("D:/programming/python/webapp/static/job_pics/" +img)
        return "<p>Image Deleted</p>"
    return render_template('images.html',img = img)

@socketio.on('connect')
def test_connect1():
    print("I'm Connected")
    if session['workscrap_var']  == 0:
        emit('not running')
        
@socketio.on('workscrap run')
def run_workscrap():
    session['workscrap_var']  = threading.Thread(target=workscrap,args=(q,))
    session['workscrap_var'].start()
    emit('running')

@socketio.on('close workscrapper')
def close_workscrapper():
    emit("my response","Workscrapper has been shut down.")
    emit("not running")
    

@socketio.on('my event')
def handle_message():
    print(q.get())
    emit('my response', q.get())

@socketio.on('disconnect')
def disconnect():
    print("I'm Disconnected")

if __name__ == '__main__':
    socketio.run(app)
    