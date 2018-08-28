from flask import render_template
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

