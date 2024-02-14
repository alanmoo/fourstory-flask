from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fourstory.db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    db.init_app(app)


    with app.app_context():
        from . import models
        db.create_all()

    # Import routes from routes.py
    from .routes import bp
    app.register_blueprint(bp)

    return app