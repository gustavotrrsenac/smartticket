from flask import Flask, request, jsonify, render_template
from flask import Blueprint

app = Flask(__name__, static_url_path='', static_folder='static')

home_bp = Blueprint("home", __name__)


app.route("/")
def home():
    return render_template('index.html')


