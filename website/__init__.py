from flask import Flask, session
import os
from .models import db, Room, User, Message
from flask_socketio import SocketIO, join_room, leave_room, send
from .routes.main import main
import datetime
from time import sleep
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

socketio = SocketIO()

def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
    #app.config['SECRET_KEY'] = 'asdAE123ASD #!2FAS 32ASD #21F 3ASD fa3 sF3ADSfa 3'

    app.register_blueprint(main, url_prefix='/')
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    socketio.init_app(app, cors_allowed_origins="*")

    return app



@socketio.on('sendingMessage')
def sendMessage(message):
    room = Room.query.filter_by(code=session.get('room_code')).first()
    user = User.query.filter_by(session_id=session.get('user')).first()
    
    if not room or not user:
        return
    
    time = datetime.datetime.now()
    time_pattern = "%Y-%m-%d %H:%M %p"
    time = time.strftime(time_pattern)


    send({"name": user.name, "message": message['message'], 'date':time}, to=room.code)

    message = Message(user_id=user.id, room_id=room.id, text=message['message'])
    db.session.add(message)
    db.session.commit()

    
    print(f"{user.name} sent a message to room {room.code}: {message}")
    
@socketio.on('connect')
def connect(auth):
    room = Room.query.filter_by(code=session.get('room_code')).first()
    user = User.query.filter_by(session_id=session.get('user')).first()
    
    if not room or not user:
        return
    
    join_room(room.code)

    time = datetime.datetime.now()
    time_pattern = "%Y-%m-%d %H:%M %p"
    time = time.strftime(time_pattern)

    
    send({"name": user.name, "message": "has entered the room", 'date':time}, to=room.code)
    
    room.users.append(user)
    db.session.commit()

    
    
    print(f"{user.name} joined the room {room.code}")
    
    
@socketio.on('disconnect')
def disconnect():
    room = Room.query.filter_by(code=session.get('room_code')).first()
    user = User.query.filter_by(session_id=session.get('user')).first()
    

    if room:
        leave_room(room.code)
        room.users.remove(user)
        #db.session.delete(user)
        db.session.commit()
        if len(room.users) <= 0:
            db.session.delete(room)
            db.session.commit()
    
    time = datetime.datetime.now()
    time_pattern = "%Y-%m-%d %H:%M %p"
    time = time.strftime(time_pattern)

    
    
    send({"name": user.name, "message": "has left the room", "date":time}, to=room.code)
    print(f"{user.name} left the room {room.code}")
        

