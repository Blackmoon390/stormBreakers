from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random
import string
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)



# Track online users per room
online_users = {}

@app.route('/')
def homee():
    return render_template('index.html')

@app.route('/create')
def create_room():
    # Generate a simple random room ID
    room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return redirect(url_for('chat_room', room_id=room_id))

@app.route('/chat/<room_id>')
def chat_room(room_id):
    return render_template('chat.html', room_id=room_id)

@socketio.on('join')
def on_join(data):
    room_id = data['room_id']
    username = data['username']
    join_room(room_id)

    if room_id not in online_users:
        online_users[room_id] = []

    # Give each user a unique color
    user_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    user_data = {'username': username, 'color': user_color}
    online_users[room_id].append(user_data)

    emit('message', {
        'sender': 'System',
        'content': f'{username} has joined the room.',
        'is_system': True,
        'timestamp': current_time()
    }, room=room_id)

    emit('user_list', online_users[room_id], room=room_id)

@socketio.on('message')
def handle_message(data):
    room_id = data['room_id']
    content = data['content']
    sender = get_username_from_sid(room_id, request.sid)

    emit('message', {
        'sender': sender,
        'content': content,
        'is_system': False,
        'timestamp': current_time(),
        'color': get_user_color(room_id, sender)
    }, room=room_id)

@socketio.on('leave')
def on_leave(room_id):
    sid = request.sid
    username = get_username_from_sid(room_id, sid)
    leave_room(room_id)

    if room_id in online_users:
        online_users[room_id] = [user for user in online_users[room_id] if user['username'] != username]
        emit('user_list', online_users[room_id], room=room_id)

        emit('message', {
            'sender': 'System',
            'content': f'{username} has left the room.',
            'is_system': True,
            'timestamp': current_time()
        }, room=room_id)

# Helper functions
def get_username_from_sid(room_id, sid):
    # This is a simplified placeholder.
    # Ideally you’d maintain a dict mapping sid -> username.
    for user in online_users.get(room_id, []):
        # In your improved version, you'd match by SID
        return user['username']
    return "Unknown"

def get_user_color(room_id, username):
    for user in online_users.get(room_id, []):
        if user['username'] == username:
            return user.get('color', '#000000')
    return '#000000'

def current_time():
    return datetime.now().strftime("%H:%M")

if __name__ == '__main__':
    socketio.run(app, debug=True)
