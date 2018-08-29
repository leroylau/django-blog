from flask import render_template, request, flash, redirect, url_for

from blog import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = int(request.form.get('pwd'))
        print(username, password)
    if username == '111' and password == 222:
        return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/blog')
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
    return render_template('blog.html', user=user, posts=posts)

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

    return f"welcome, {username}!"
