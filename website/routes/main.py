from flask import Blueprint, redirect, render_template, url_for, request, session, flash
import random
import string
from ..models import Room, db, User, Message
import uuid

main = Blueprint('main', __name__)


def generate_room_code(length):
    while True:
        code = ''
        for _ in range(length):
            code += random.choice(string.digits)
            
        room = Room.query.filter_by(code=code).first()
        if not room:
            break
    return code


@main.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing-page.html')        


@main.route('/home', methods=['GET', 'POST'])
def home():
    """"main home page rendered function"""
    session.clear()
    if request.method == 'POST':
        if session.get('session_key') is None:
            session['session_key'] = str(uuid.uuid4())
        print(f"session_key is {session['session_key']}")
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)
        
        if not name:
            flash("Please enter a name", category='danger')
            return render_template('home.html', name=name, code=code)
        
        if join != False and not code:
            flash('Please enter a room code to join', category='danger')
            return render_template('home.html', name=name, code=code)
        
        
        
        if create != False:
            user = User(name=name, session_id=session['session_key'])
            room = Room(code=generate_room_code(4))
            user.room_code = room.code
            db.session.add(room)
            db.session.add(user)
            db.session.commit()
            session['room_code'] = room.code
            session['user_name'] = name
            session['user'] = user.session_id
            return redirect(url_for('main.room'))
        room = Room.query.filter_by(code=code).first()
        if room:
            user = User(name=name, session_id=session['session_key'], room_code=room.code)
            db.session.add(user)
            db.session.commit()
            session['room_code'] = room.code
            session['user_name'] = name
            session['user'] = user.session_id
            return redirect(url_for('main.room'))
        flash('Room not found', category='danger')
        return render_template('home.html', name=name, code=code)
    
    return render_template('home.html')


@main.route('/room')
def room():
    room_code = session.get('room_code')
    room = Room.query.filter_by(code=room_code).first()
    
    if room is None or session.get('user_name') is None or room_code is None:
        return redirect(url_for('main.home'))
    users = room.users
    messages = Message.query.filter_by(room_id=room.id).all()
    return render_template('room.html', code=room.code, users=users, messages=messages)