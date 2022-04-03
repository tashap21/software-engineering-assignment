from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    events = db.relationship('Event', backref='user', passive_deletes=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(30))
    eventtime = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    # foreign key is used to make sure that the user exists
    creator = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
