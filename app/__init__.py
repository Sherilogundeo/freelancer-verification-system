import os
from flask import Flask, redirect, request, url_for

from app.config import DevelopmentConfig, ProductionConfig
from .extensions import db, login_manager, mail

from .blueprints.index import index_bp
from .blueprints.auth import auth_bp
from .blueprints.dashboard import dashboard_bp
from .blueprints.admin import admin_bp

def create_app():
    app = Flask(__name__)

    # Determine the environment and load the correct config
    env = os.getenv('FLASK_ENV', 'production').lower()
    if env == "development":
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    @login_manager.unauthorized_handler
    def unauthorized():
        # If an admin hits an admin route → send them to admin-login
        if request.path.startswith("/admin"):
            return redirect(url_for("auth.admin_login", next=request.path))

        # Otherwise → normal login
        return redirect(url_for("auth.login", next=request.path))

    return app