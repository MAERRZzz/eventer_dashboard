from flask import Flask

from apps.config import Config
from apps.errors import errors
from apps.auth.auth import auth_bp
from apps.user.user_bp import user_bp
from apps.home.home_bp import home_bp
from apps.organizer.organizer_bp import organizer_bp
from apps.event.event_bp import event_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(organizer_bp)
    app.register_blueprint(event_bp)

    app.register_blueprint(errors.errors_bp)  # 403/404/500 errors
