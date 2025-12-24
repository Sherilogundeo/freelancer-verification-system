from uuid import uuid4
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Allows Flask-Login to load BOTH User and SuperUser correctly."""
    from app.blueprints.admin.models import SuperUser  # local import to avoid circular import

    # Try normal user
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return user

    # Try admin
    return SuperUser.query.filter_by(super_id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.String(64),
        unique=True,
        default=lambda: str(uuid4()),
        nullable=False
    )

    email = db.Column(db.String(60), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(40))
    phone = db.Column(db.String(20), unique=True)
    profile = db.Column(db.String(64), default="default-avatar.png")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.user_id

    # --------------------------
    # Represent
    # --------------------------
    def __repr__(self):
        return f"<User {self.username}>"

    # --------------------------
    # Password
    # --------------------------
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # --------------------------
    # CRUD Helpers
    # --------------------------
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # --------------------------
    # Reset Token
    # --------------------------
    def get_reset_token(self, max_age=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        expires = datetime.utcnow() + timedelta(seconds=max_age)

        return s.dumps({
            "user_id": self.user_id,
            "exp": int(expires.timestamp())
        })

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            return None

        if data["exp"] < int(datetime.utcnow().timestamp()):
            return None

        return User.query.filter_by(user_id=data["user_id"]).first()


    def reg_date(self):
        return self.created_at.strftime('%Y-%m-%d')