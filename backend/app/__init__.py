from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    CORS(
        app, resources={r"/*": {"origins": [r"http://localhost:*"]}},
    )
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # call init_app to complete initialization
    db.init_app(app)
    login_manager.init_app(app)

    # create app blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .events import events as events_blueprint

    app.register_blueprint(events_blueprint, url_prefix="/events")

    from .companies import companies as companies_blueprint

    app.register_blueprint(companies_blueprint, url_prefix="/companies")

    from .users import users as users_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/users")

    from .account import account as account_blueprint

    app.register_blueprint(account_blueprint, url_prefix="/account")

    return app
