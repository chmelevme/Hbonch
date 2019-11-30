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
    from auth import routes
    app.register_blueprint(routes.auth)
    from user_profile import routes
    app.register_blueprint(routes.profile)
    from webapp.models import User, Deadline, Level, Group, Deadline_status
    return app
