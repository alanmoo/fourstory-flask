from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
import os

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    # Fix for when the app is behind GCP proxy, as the auth request url for foursquare ends up being http otherwise
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}"
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    db.init_app(app)


    with app.app_context():
        from . import models
        db.create_all()

    # Import routes from routes.py
    from .routes import bp
    app.register_blueprint(bp)

    return app