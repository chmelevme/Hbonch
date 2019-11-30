from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(app_config=config):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(app_config)
    db.init_app(app=app)
    migrate.init_app(app, db)
    login.init_app(app)


    return app
