from flask import render_template
from . import app

@app.route('/<name>')
def hello(name):
    return render_template('hello.html', name=name)