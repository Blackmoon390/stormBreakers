from pydoc import doc
from traceback import print_tb
from flask import Flask,render_template,jsonify,request
import os
import shutil
import speech_recognition as sr
import VOICE_AI
import database_admin



app=Flask(__name__)

@app.route('/')
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

@app.route('/bear.html')
def bear():
    return render_template("bear.html")

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
    voiceprocess=VOICE_AI.Voice_Generator(text)  # Call the content model to get a response

    


    return jsonify({
    "text": text,
    "audio_url": f"/static/audio/responses/response.wav"})

@app.route('/tell-story')
def tell_story():

    return jsonify({
        "audio_url": f"/static/audio/story.wav"
    })



@app.route('/leaderboard')
def leaderboard():
    # Get your data from database or other source
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
@app.route('/consultant.html')
def consultant():
    doctors=database_admin.show_users()
    return render_template('consultant.html', doctors=doctors)

@app.route('/api/notify', methods=['POST'])
def notify_doctor():
    data = request.json
    
    # Print the notification to console
    print(f"Doctor called: {data.get('name')} - {data.get('email')} - {data.get('phone')}")
    print(f"Message: {data.get('message')}")
    print(f"Timestamp: {data.get('timestamp')}")
    
    return jsonify({
        "success": True, 
        "message": f"Successfully notified {data.get('name')}"
    })



if __name__== '__main__':
    app.run(debug=True)

