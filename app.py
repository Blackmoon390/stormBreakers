from pydoc import doc
from traceback import print_tb
from flask import Flask,render_template,jsonify,request,session,redirect,url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import os
import shutil
import speech_recognition as sr
import VOICE_AI
import database_admin
import Emailer
import random
import string




app=Flask(__name__)

users = {
    "Alex": "1234",
    "Brent": "5678"  # You can change this password if needed
}


@app.route('/')
def logger():
    
    if 'username' in session:
        return redirect(url_for('home'))

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data directly
        username = request.form['username']
        password = request.form['password']

        
        # Check if username exists and password is correct
        if username in users and users[username] == password:
            return redirect(url_for('home'))

        
    return render_template('login.html')

@app.route('/mainpage.html')
def home():
    return render_template('mainpage.html')

@app.route('/tic_tac_toe.html')
def tixtactoe():
    return render_template('tic_tac_toe.html')

@app.route('/flipcard.html')
def flipcards():
    return render_template('flipcard.html')

@app.route('/games.html')
def quiz():
    return render_template('games.html')

UPLOAD_DIR = "static/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

num=None  # Initialize num variable

@app.route('/bear.html', methods=['GET', 'POST'])
def bear_companian():
    message = ""
    if request.method == 'POST':
        selected = request.form.get('option')
        if selected == 'option1':
            num = 0
        elif selected == 'option2':
            num = 1
        else:
            message = "Please select an option."
    return render_template('bear.html', message=message)

@app.route('/roleplay.html')
def roleplay():
    return render_template("roleplay.html")


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
        except Exception as e:
            text = "Could not recognize speech."


    response_audio = os.path.join(UPLOAD_DIR, 'response.wav')
    voiceprocess=VOICE_AI.Voice_Generator(text,num)  # Call the content model to get a response

    


    return jsonify({
    "text": text,
    "audio_url": f"/static/audio/responses/response.wav"})

@app.route('/tell-story')
def tell_story():
    number = random.randint(1, 5)
    story_name = "story" + str(number) + ".wav"

    return jsonify({
        "audio_url": f"/static/audio/{story_name}"
    })



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
    
    # Use your own column headers
    column1_header = "Child"  # or any header you want
    column2_header = "Stars"  # or any header you want
    
    return render_template(
        'leaderboard.html',
        users=users,
        column1_header=column1_header,
        column2_header=column2_header
    )
@app.route('/consultation.html')
def consultant():
    doctors=database_admin.show_users()
    return render_template('consultation.html', doctors=doctors)

@app.route('/api/notify', methods=['POST'])
def notify_doctor():
    data = request.json
    Emailer.mail_sender(data.get('email'))
    #Print the notification to consol/
    print(f"Doctor called: {data.get('name')} - {data.get('email')} - {data.get('phone')}")
    
    
    return jsonify({
        "success": True, 
        "message": f"Successfully notified {data.get('name')}"
    })


@app.route('/memberslist.html')
def memberslist():
    users = ['vishnu', 'micheal', 'madhan']
    return render_template('memberslist.html', users=users)

@app.route('/chat/<username>')
def chat_with_user(username):
    return render_template('chat.html', username=username)


correct_password = "1234"  # Replace with your actual password
tasks = {
    "task1": "Complete project setup",
    "task2": "Design database schema",
    "task3": "Implement user authentication",
    "task4": "Develop main features",
    "task5": "Write tests and documentation",
}

def calculate_progress(completed_tasks):
    """Calculates the progress percentage and score."""
    total_tasks = len(tasks)
    completed_count = len(completed_tasks)
    progress = (completed_count / total_tasks) * 100 if total_tasks else 0
    score = completed_count * 10
    return progress, score

@app.route('/task_page1.html', methods=['GET', 'POST'])
def task_tracker():
    """Handles task tracker display and submission."""
    password_message = ""
    completed_tasks = session.get('completed_tasks', [])
    progress = session.get('progress', 0)  # Load progress from session
    score = session.get('score', 0)  # Load score from session

    if request.method == 'POST':
        if 'verify' in request.form and request.form['verify'] == 'true':
            password = request.form.get('password')
            if password == correct_password:
                session['verified'] = True
                password_message = "Password is correct!"
            else:
                password_message = "Incorrect password. Please try again."
            return render_template('task_page1.html', tasks=tasks, completed_tasks=completed_tasks, progress=progress, score=score, password_message=password_message)

        if 'complete' in request.form:
            if session.get('verified'):
                if 'tasks' in request.form:
                    completed_tasks = request.form.getlist('tasks')
                    session['completed_tasks'] = completed_tasks
                progress, score = calculate_progress(completed_tasks)
                session['progress'] = progress  # Save progress to session
                session['score'] = score  # Save score to session
                return render_template('task_page1.html', tasks=tasks, completed_tasks=completed_tasks, progress=progress, score=score, password_message="Password is correct!")
            else:
                password_message = "Please verify the password to complete the task."
                return render_template('task_page1.html', tasks=tasks, completed_tasks=completed_tasks, progress=progress, score=score, password_message=password_message)

        if 'exit' in request.form:
            session['verified'] = False
            password_message = "Tasks locked. Please verify password to continue."
            return render_template('task_page1.html', tasks=tasks, completed_tasks=[], progress=0, score=0, password_message=password_message)

    return render_template('task_page1.html', tasks=tasks, completed_tasks=completed_tasks, progress=progress, score=score, password_message=password_message)



# Track online users per room
online_users = {}

@app.route('/index.html')
def homeCall():
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



if __name__== '__main__':
    app.run(debug=True)
