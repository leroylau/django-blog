from flask import render_template, url_for
from flaskr.post import blog

@blog.route('/')
@blog.route('/index')
def index():
    return render_template('post/index.html')

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
    return render_template('post/user.html', name=name, posts=posts)