from . import db
from sqlalchemy.sql import func

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())