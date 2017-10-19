from flask import Flask, render_template, request, redirect, url_for, session, flash
import quickstart
import simplejson as json # for output formatting
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://booking_app:1234@localhost:8889/booking_app'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'xy337KGys&'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    serviceType = db.Column(db.String(220))

    def __init__(self, firstName, lastName, email, address, serviceType):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.address = address
        self.serviceType = serviceType

# Event class
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    start = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    end = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __init__(self, title, start, end, user_id):
        self.title = title
        self.start = start
        self.end = end
        self.user_id = user_id

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == 'GET'):
        return render_template('signup.html')
    if (request.method == 'POST'):
        username = request.form['firstname']
        password = request.form['password']
        verifypassword = request.form['verifypassword']
        if (len(username) < 3):
            return render_template('signup.html', name_error="user field is empty or too short", first_name=username)
        if (len(password) < 3):
            return render_template('signup.html', pwd_error="password field is empty or too short", first_name=username)
        if (len(verifypassword) == 0):
            return render_template('signup.html', vpwd_error="verify password field is blank", first_name=username)
        if (password != verifypassword):
            return render_template('signup.html', vpwd_error="passwords don't match", first_name=username)
        exisiting_user = User.query.filter_by(username = username).first()
        if not exisiting_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/login')
        else:
            return render_template('signup.html', name_error="user already exists", user_name=username)

@app.route("/")
@app.route('/home')
def index():
    events = {"a": "aa"}#quickstart.main()
    #print(json.dumps(events, indent=2))
    # (events)
    return render_template('index.html', events=events)

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/form")
def form():
    return render_template('form.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        userobject = User.query.filter_by(username = username).first()
        if userobject:
            if userobject.password == password:
                session['username'] = username
                return redirect('/home')
            else:
                return render_template('login.html', pwd_error="wrong password", usernamevalue= username)
        else:
            return render_template('login.html', uname_error="user doesn't exist", usernamevalue= username)
@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/home')

if __name__ == '__main__':
    app.run()
