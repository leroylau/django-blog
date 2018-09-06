import json, os

from flask import flash, redirect, render_template, request, session, url_for

from blog import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = int(request.form.get('pwd'))
        with open("/Users/liuchang/Documents/Projects/WebProgrammingWithPythonAndjavaScript/projects/flask-tutorial" + "/user.json", 'r') as f:
            users = json.load(f)
            if (username in users) and (password == users[username]):
                session['username'] = username
                return redirect(url_for('blog'))
    return render_template('login.html')

@app.route('/blog')
def blog():
    user = {'name' : session['username']}
    with open("/Users/liuchang/Documents/Projects/WebProgrammingWithPythonAndjavaScript/projects/flask-tutorial" + "/blog.json", 'r') as f:
        blogs = json.load(f)
        posts = blogs[session['username']]
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
