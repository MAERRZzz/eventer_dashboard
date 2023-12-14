from flask import Flask

from app.config import Config
from app.blueprints.registration.registration_bp import registration_bp
from app.blueprints.login.login_bp import login_bp
from app.blueprints.logout.logout_bp import logout_bp

from app.blueprints.home.home_bp import home_bp
from app.blueprints.event.event_bp import event_bp
from app.blueprints.user.user_bp import user_bp
from app.blueprints.organizer.organizer_bp import organizer_bp


def register_extensions(app):
    pass


def register_blueprints(app):
    app.register_blueprint(registration_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)

    app.register_blueprint(home_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(organizer_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SECURE=True)

    register_extensions(app)
    register_blueprints(app)

    return app
