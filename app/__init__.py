
# Utilities
import os

# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# App
from app.database import db
from app.config import Config
from app.models import Book
from .config import Config

PWD = os.path.abspath(os.curdir)


def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{}/dbase.db'.format(PWD)
    db.init_app(app)

    return app
