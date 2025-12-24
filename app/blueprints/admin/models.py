from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class SuperUser(db.Model, UserMixin):
    __tablename__ = 'superuser'

    id = db.Column(db.Integer, primary_key=True)
    super_id = db.Column(
        db.String(64),
        unique=True,
        default=lambda: str(uuid4()),
        nullable=False
    )

    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return self.super_id

    def __repr__(self):
        return f"<SuperUser {self.email}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
