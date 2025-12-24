from uuid import uuid4
from datetime import datetime, timedelta
from app import db

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text())
    user_id = db.Column(db.String(), db.ForeignKey('user.user_id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()