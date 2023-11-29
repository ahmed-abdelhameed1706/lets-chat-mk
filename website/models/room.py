from . import db
from sqlalchemy.sql import func

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    users = db.relationship('User')
    messages = db.relationship('Message')
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())