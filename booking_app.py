from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.config['DEBUG'] = True

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')

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

app.run()
