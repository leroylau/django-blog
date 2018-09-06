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

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/blog')
def blog():
    if 'username' in session:
        user = {'name' : session['username']}
        with open("/Users/liuchang/Documents/Projects/WebProgrammingWithPythonAndjavaScript/projects/flask-tutorial" + "/blog.json", 'r') as f:
            blogs = json.load(f)
            posts = blogs[session['username']]
        return render_template('blog.html', user=user, posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = int(request.form.get('pwd'))
    
        error = None
        if not username:
            error = 'Please enter your name.'
        if not email:
            error = 'Please enter your email.'
        if not password:
            error = 'Please enter your password.'

        flash(error)

        with open("/Users/liuchang/Documents/Projects/WebProgrammingWithPythonAndjavaScript/projects/flask-tutorial" + "/user.json", 'w+') as f:
            users = json.load(f)
            users[username] = password
            json.dump(users, f)
            flash("注册成功！")
        with open("/Users/liuchang/Documents/Projects/WebProgrammingWithPythonAndjavaScript/projects/flask-tutorial" + "/blog.json", 'w+') as f:
            blogs = json.load(f)
            blogs[username] = []
            json.dump(blogs, f)
            return redirect(url_for('login'))
    return render_template('register.html')