from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Please log in to continue."
login_manager.blueprint_login_views = {
    "admin": "/auth/admin-login"
}
mail = Mail()
