from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# function that creates the application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secretkey"

    from .pages import pages
    from .auth import auth

    app.register_blueprint(pages, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
