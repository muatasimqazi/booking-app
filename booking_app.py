from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json # for output formatting
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://booking_app:1234@localhost:8889/booking_app'
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
app.secret_key = 'xy337KGys&'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    events = db.relationship('Event', backref='owner')

    def __init__(self, username, password, first_name, last_name, email, address):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address


# event class
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    start = db.Column(db.String(120))
    end = db.Column(db.String(120))
    description = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, start, end, description, owner):
        self.title = title
        self.start = start
        self.end = end
        self.description = description
        self.owner = owner

# customer
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    zip_code = db.Column(db.Integer)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    #event = db.relationship('Event', backref='owner')

    def __init__(self, first_name, last_name, email, phone_number, address, zip_code, city, state):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.state = state

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    brand = db.Column(db.String(120))
    serial = db.Column(db.String(120))
    model = db.Column(db.String(120))
    filterSize = db.Column(db.Integer)

    def __init__(self, brand, serial, model, filterSize):
        self.brand = brand
        self.serial = serial
        self.model = model
        self.filterSize = filterSize

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == 'GET'):
        return redirect('/')
    if (request.method == 'POST'):
        username = request.form['username']
        first_name = request.form['first-name']
        password = request.form['password']
        last_name = request.form['last-name']
        verify_password = request.form['verify-password']
        email = request.form['email']
        address = request.form['address']

        subject = request.form.get('username')
        useraddress = request.form.get('address')
# NOTE: Change the email address for sender and recipients
        msg = Message(subject,sender='your_email@gmail.com',recipients=['recipients_email@live.com'])
        msg.body = useraddress
        # mail.send(msg)

        username_error = ''
        email_error = ''
        exisiting_email_error = ''
        verify_error = ''

        if len(username)>=120 or len(username)==0:
            username_error = "Invalid user name please enter a valid user name"
            return username_error

        if len(email)>=120 or len(email)==0:
            email_error = "Please enter a valid email"
            return email_error

        if len(email_error)>0:
            return "Please try again"

        if password != verify_password:
            verify_error = "password does not match, please try again"
            return verify_error

        username_error = ''
        email_error = ''
        exisiting_email_error = ''
        verify_error = ''

        if len(username)>=120 or len(username)==0:
            username_error = "Invalid user name please enter a valid user name"
            return username_error
            
        if len(email)>=120 or len(email)==0:
            email_error = "Please enter a valid email"
            return email_error

        if len(email_error)>0:
            return "Please try again"

        if password != verify_password:
            verify_error = "password does not match, please try again"
            return verify_error

        exisiting_user = User.query.filter_by(username = username).first()
        if not exisiting_user:
            new_user = User(username, password, first_name, last_name, email, address)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            return render_template('index.html', name_error="user already exists", user_name=username)

@app.route("/")
@app.route('/home')
def index():

    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('index.html', user=user)

    return render_template('index.html')

# creates event / booking
@app.route('/new_booking', methods=['POST'])
def new_booking():
    if request.method == 'POST':
        username = session['username']
        owner = User.query.filter_by(username=username).first()
        event_title = request.form['event-title']
        event_date = request.form['event-date']
        event_time = request.form['event-time']
        event_start = event_date + 'T' + event_time
        event_end = int((event_time).split(':')[0]) + 2

        event_end = event_date + 'T' + str(event_end) + ':00'
        event_description = request.form['description']

        event_new = Event(event_title, event_start, event_end, event_description, owner)
        db.session.add(event_new)
        db.session.commit()
        # event_id = event_new.id;
    return redirect('/book')

def toList(self):
    event = {'id': self.id, 'title': self.title, 'start': self.start, 'end': self.end, 'description': self.description, 'color': 'purple', 'className': '' }
    return event

# shows the user's booking schedule
@app.route('/_get_events', methods=['GET', 'POST'])
def get_events():
    username = session['username']
    if not username:
        pass

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
    return redirect('/book')


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

@app.route("/book/", methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        new_booking()
    if request.method == 'GET' and request.args.get('id'):
        event_id = request.args.get('id')
        del_event(event_id)

    return render_template('booking.html')
if __name__ == '__main__':
    app.run()
