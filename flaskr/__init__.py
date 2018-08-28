from flask import Flask
from flaskr.post import blog

app = Flask(__name__)
app.register_blueprint(blog)
