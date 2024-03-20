from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
from user.models import User

app = Flask(__name__)
app.secret_key = b'\xca\xfc\x17\xbd\xda\x15\xf9\x16[\xc2\x08\xbaP\x8d\xf8\xa1'

client = pymongo.MongoClient('localhost', 27017)
db = client.test_user

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/users/signup', methods = ['POST'])
def signup():
    return User().signup()

@app.route('/user/login', methods = ['POST'])
def login():
    return User().login()

@app.route('/user/signout')
def signout():
    return User().signout()



if __name__ == "__main__":
    app.run(debug=True)