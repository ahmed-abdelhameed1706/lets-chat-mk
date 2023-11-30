from flask import Flask, session
import os
from .models import db, Room, User
from flask_socketio import SocketIO, join_room, leave_room, send
from .routes.main import main
import datetime
from time import sleep

app = Flask(__name__)


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')

    app.register_blueprint(main, url_prefix='/')
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app


app = create_app()

socketio = SocketIO(app)

@socketio.on('connect')
def connect(auth):
    room = Room.query.filter_by(code=session.get('room_code')).first()
    user = User.query.filter_by(session_id=session.get('user')).first()
    
    if not room or not user:
        return
    
    join_room(room.code)
    
    send({"name": user.name, "message": "has entered the room"}, to=room.code)
    
    room.users.append(user)
    db.session.commit()
    
    print(f"{user.name} joined the room {room.code}")
    
    
@socketio.on('disconnect')
def disconnect():
    room = Room.query.filter_by(code=session.get('room_code')).first()
    user = User.query.filter_by(session_id=session.get('user')).first()
    leave_room(room.code)

    if room:
        room.users.remove(user)
        #db.session.delete(user)
        db.session.commit()
        if len(room.users) <= 0:
            db.session.delete(room)
            db.session.commit()
    
    
    send({"name": user.name, "message": "has left the room"}, to=room.code)
    print(f"{user.name} left the room {room.code}")
        

