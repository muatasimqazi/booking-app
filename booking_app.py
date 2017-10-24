from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json # for output formatting
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
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    serviceType = db.Column(db.String(220))
    events = db.relationship('Event', backref='owner')

    def __init__(self, username, password, firstName, lastName, email, address, serviceType):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.address = address
        self.serviceType = serviceType

# event class
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    start = db.Column(db.String(120))
    end = db.Column(db.String(120))
    description = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, start, end, owner):
        self.title = title
        self.start = start
        self.end = end
        self.owner = owner

# customer
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    zipCode = db.Column(db.Integer(5))
    city = db.Column(db.Sting(100))
    state = db.Colum(db.String(100))
    event = db.relationship('Event', backref='owner')

    def __init__(self, firstName, lastName, email, phoneNumber, address, zipCode, city, state):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.zipCode = zipCode
        self.city = city
        self.state = state



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == 'GET'):
        return redirect('/')
    if (request.method == 'POST'):
        username = request.form['username']
        firstname = request.form['firstname']
        password = request.form['password']
        lastname = request.form['lastname']
        verifypassword = request.form['verifypassword']
        email = request.form['email']
        address = request.form['address']
        serviceType = request.form['servicetype']
        if (len(username) < 3):
            return render_template('index.html', name_error="user field is empty or too short", first_name=username)
        if (len(password) < 3):
            return render_template('index.html', pwd_error="password field is empty or too short", first_name=username)
        if (len(verifypassword) == 0):
            return render_template('index.html', vpwd_error="verify password field is blank", first_name=username)
        if (password != verifypassword):
            return render_template('index.html', vpwd_error="passwords don't match", first_name=username)
        exisiting_user = User.query.filter_by(username = username).first()
        if not exisiting_user:
            new_user = User(username, password, firstname, lastname, email, address, serviceType)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            return render_template('index.html', name_error="user already exists", user_name=username)

@app.route("/", methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():

    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if request.method == 'POST':
            create_event()

        if request.method == 'GET' and request.args.get('id'):
            event_id = request.args.get('id')
            del_event(event_id)

        return render_template('index.html', user=user)
    return render_template('index.html')

# creates event / booking
@app.route('/createevent', methods=['POST'])
def create_event():
    username = session['username']
    owner = User.query.filter_by(username=username).first()
    event_title = request.form['event-title']
    event_date = request.form['event-date']
    event_start = event_date + 'T' + request.form['event-start']
    event_end = event_date + 'T' + request.form['event-end']

    event_new = Event(event_title, event_start, event_end, owner)
    db.session.add(event_new)
    db.session.commit()
    event_id = event_new.id;
    return redirect('/')

def toList(self):
    event = {'id': self.id, 'title': self.title, 'start': self.start, 'end': self.end, 'color': 'purple', 'className': '' }
    return event

# shows the user's booking schedule
@app.route('/_get_events', methods=['GET', 'POST'])
def get_events():
    username = session['username']
    owner = User.query.filter_by(username=username).first()

    events = Event.query.filter_by(owner=owner).all()
    events_feed = []
    for item in events:
        events_feed.append(toList(item))
    return jsonify(events_feed)

# deletes a booked appointment
def del_event(event_id):
    delete_event = Event.query.filter_by(id=event_id).first();
    db.session.delete(delete_event)
    db.session.commit();
    return redirect('/home')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        username_error = ''
        password_error = ''
        if user:
            if user.password == password:
                session['username'] = username
                print(session['username'])
                return redirect('/')

            if user.password != password :
                password_error = 'Incorrect password'

        else:
            username_error = "This username does not exist"

        return render_template('login.html', username_error=username_error, password_error=password_error)

    return render_template('login.html')
@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/home')

if __name__ == '__main__':
    app.run()
