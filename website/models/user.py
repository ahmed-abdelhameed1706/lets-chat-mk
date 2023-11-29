from . import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    room_code = db.Column(db.String(10), db.ForeignKey('room.code'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    messages = db.relationship('Message')