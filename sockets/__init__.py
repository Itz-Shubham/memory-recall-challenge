from flask import session
from flask_login import current_user
from flask_socketio import SocketIO, join_room, leave_room, send
from models import db, Score
from string import ascii_uppercase
import random

COLORS = ["YELLOW", "RED", "GREEN", "PURPLE"]

room_ids_for_anonymous_user = []
socketio = SocketIO()

@socketio.on('connect')
def connect():
    roomId = getRoomId()
    join_room(room=roomId)
    session['game_seq'] = []
    new_color = generateNextColor()
    send(jsonMessage('start', new_color), to=roomId)


@socketio.on('restart')
def restart():
    session['game_seq'] = []
    new_color = generateNextColor()
    send(jsonMessage('start', new_color), to=getRoomId())


@socketio.on('submit_colors')
def submit_colors(colors):
    if colors == session['game_seq']:
        new_color = generateNextColor()
        send(jsonMessage('level_up', new_color), to=getRoomId())
    else:
        send(jsonMessage('game_over', None))
        if current_user.is_authenticated:
            new_score = len(session['game_seq'])-1
            score = Score.query.filter_by(user_id=current_user.id).first()
            if not score:
                score = Score(user_id=current_user.id, attempts=1, high_score=new_score)
            elif score and score.high_score < new_score:
                score.high_score = new_score
                score.attempts+=1
            db.session.add(score)
            db.session.commit()
        session['game_seq'] = []


@socketio.on('disconnect')
def disconnect():
    roomId = getRoomId()
    if not current_user.is_authenticated:
        room_ids_for_anonymous_user.remove(roomId)
    leave_room(roomId)


def jsonMessage(game_status:str, new_color:str):
    return {
        'game_status': game_status,
        'new_color':new_color,
        'current_level': len(session['game_seq']),
    }


def generateNextColor():
    new_color = random.choice(COLORS)
    session['game_seq'].append(new_color)
    return new_color


def getRoomId() -> str:
    if current_user.is_authenticated:
        room_id = f"game_room_{current_user.id}"
    else:
        room_id = session.get('player_room')
        if not room_id:
            room_id = generateUniqueRoomId()
            room_ids_for_anonymous_user.append(room_id)
        session['player_room'] = room_id
    return room_id

        
def generateUniqueRoomId():
    while True:
        unique_id = "game_room_"
        for _ in range(5):
            unique_id += random.choice(ascii_uppercase)
        if unique_id not in room_ids_for_anonymous_user:
            break
    return unique_id