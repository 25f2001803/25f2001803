from flask import Flask
from routes import auth, admin, staff, user
from extensions import login_manager
from models.user import User
from config import Config
from extensions import db
import models


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(staff)
    app.register_blueprint(user)

    @app.route("/")
    def home():
        return "<h1>Welcome to Trekking Management Application</h1>"

    return app