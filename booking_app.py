from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://booking_app:booking@localhost:8889/booking_app'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'xy337KGys&'
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == 'GET'):
        return render_template('signup.html')
    if (request.method == 'POST'):
        username = request.form['icon_prefix']
        password = request.form['icon_password']
        verifypassword = request.form['icon_verifypassword']
        if (len(username) < 3):
            return render_template('signup.html', name_error="user field is empty or too short", user_name=username)
        if (len(password) < 3):
            return render_template('signup.html', pwd_error="password field is empty or too short", user_name=username)
        if (len(verifypassword) == 0):
            return render_template('signup.html', vpwd_error="verify password field is blank", user_name=username)
        if (password != verifypassword):
            return render_template('signup.html', vpwd_error="passwords don't match", user_name=username)
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
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run()
