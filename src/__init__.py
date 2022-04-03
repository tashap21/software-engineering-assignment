from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "users.db"


# function that creates the application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .pages import pages
    from .auth import auth

    app.register_blueprint(pages, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)

    # redirects the user to the login page if they haven't logged in
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # function for the login manager to find the user model
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# function that creates the database if it doesn't already exist
def create_database(app):
    if not path.exists("src/" + DB_NAME):
        db.create_all(app=app)
