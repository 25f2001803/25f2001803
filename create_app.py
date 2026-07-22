from flask import Flask

from config import Config
from extensions import db
import models


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def home():
        return "<h1>Welcome to Trekking Management Application</h1>"

    return app