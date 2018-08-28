from flask import render_template, url_for
from flaskr.blog import blog

@blog.route('/')
@blog.route('/index')
def index():
    return render_template('blog/index.html')

@blog.route('/<name>')
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
    return render_template('blog/user.html', name=name, posts=posts)