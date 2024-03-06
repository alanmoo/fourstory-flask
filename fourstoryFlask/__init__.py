from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

load_dotenv()

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fourstory.db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['FOURSQUARE_CLIENT_ID'] = os.getenv('FOURSQUARE_CLIENT_ID')
    app.config['FOURSQUARE_CLIENT_SECRET'] = os.getenv('FOURSQUARE_CLIENT_SECRET')
    db.init_app(app)


    with app.app_context():
        from . import models
        db.create_all()

    # Import routes from routes.py
    from .routes import bp
    app.register_blueprint(bp)

    return app
