from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room
import os
import shutil
import speech_recognition as sr
import VOICE_AI
import database_admin
import Emailer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Home route
@app.route('/')
def home():
    return render_template('mainpage.html')

# Other static routes for games and consultation pages
@app.route('/tic_tac_toe.html')
def tixtactoe():
    return render_template('tic_tac_toe.html')

@app.route('/flipcard.html')
def flipcards():
    return render_template('flipcard.html')

@app.route('/games.html')
def quiz():
    return render_template('games.html')

# Upload directory for audio files
UPLOAD_DIR = "static/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/bear.html')
def bear():
    return render_template("bear.html")

# Upload route for speech recognition
@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join(UPLOAD_DIR, 'uploaded.wav')
    audio_file.save(audio_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
        except Exception:
            text = "Could not recognize speech."

    VOICE_AI.Voice_Generator(text)  # Generates response.wav

    return jsonify({
        "text": text,
        "audio_url": f"/static/audio/responses/response.wav"
    })

# Route to tell a story
@app.route('/tell-story')
def tell_story():
    return jsonify({
        "audio_url": f"/static/audio/story.wav"
    })

# Leaderboard route
@app.route('/leaderboard.html')
def leaderboard():
    users = [
        ["Luna", 1520],
        ["Oliver", 1340],
        ["Mia", 1190],
        ["Noah", 980],
        ["Emma", 870],
        ["Liam", 760]
    ]
    return render_template('leaderboard.html', users=users, column1_header="Child", column2_header="Stars")

# Consultation route
@app.route('/consultation.html')
def consultant():
    doctors = database_admin.show_users()
    return render_template('consultation.html', doctors=doctors)

# Notify doctor route
@app.route('/api/notify', methods=['POST'])
def notify_doctor():
    data = request.json
    Emailer.mail_sender(data.get('email'))
    return jsonify({
        "success": True,
        "message": f"Successfully notified {data.get('name')}"
    })

# Members list route
@app.route('/memberslist.html')
def memberslist():
    users = ['vishnu', 'micheal', 'madhan']
    return render_template('memberslist.html', users=users)

# Chat route for each user
@app.route('/chat/<receiver>')
def chat_with_user(receiver):
    sender = request.args.get('sender', 'Anonymous')
    room = f"{sender}_{receiver}"  # Unique room name
    return render_template('chat.html', sender=sender, receiver=receiver, room=room)

# --- SocketIO Chat Events ---
@socketio.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)
    print(f"User joined room: {room}")

@socketio.on('send_message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    # Emit the message to everyone in the room
    emit('receive_message', {'username': username, 'message': message}, room=room)

@socketio.on('leave_room')
def on_leave(data):
    room = data['room']
    print(f"User left room: {room}")

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)
