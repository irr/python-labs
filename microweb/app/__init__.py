from flask import Flask

microweb = Flask(__name__)

from app import views
