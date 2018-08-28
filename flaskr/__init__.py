from flask import Flask
from flaskr.blog import blog

app = Flask(__name__)
app.register_blueprint(blog)
