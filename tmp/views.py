from flask import render_template
from flaskr import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/<name>')
def user(name):
    posts = [
        {
            'name' : 'william',
            'body' : "A lovely day."
        },
        {
            'name' : 'william',
            "body" : 'A trip to Japan.'
        }
    ]
    return render_template('user.html', name=name, posts=posts)