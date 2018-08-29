from flask import render_template, request, flash

from blog import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    user = {'name' : 'william'}
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
    return render_template('user.html', user=user, posts=posts)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['pwd']
    
    error = None
    if not username:
        error = 'Please enter your name.'
    if not email:
        error = 'Please enter your email.'
    if not password:
        error = 'Please enter your password.'

    flash(error)

    return f"welcome {username}!"
