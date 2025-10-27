from flask import Flask
from flask_cors import CORS
from .routes import bp
app = Flask(__name__)
CORS(app, origins="*")
app.register_blueprint(bp)
