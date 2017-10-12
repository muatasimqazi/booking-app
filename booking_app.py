from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404

@app.route("/")
def index():
    return render_template('base.html')

app.run()
