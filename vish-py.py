from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for sessions

# Dummy task list
tasks = {
    "task1": "Complete project setup",
    "task2": "Design database schema",
    "task3": "Implement user authentication",
    "task4": "Develop main features",
    "task5": "Write tests and documentation",
}

correct_password = "1234"  # Change as needed

def calculate_progress(completed_tasks):
    total_tasks = len(tasks)
    completed_count = len(completed_tasks)
    progress = (completed_count / total_tasks) * 100 if total_tasks else 0
    score = completed_count * 10
    return progress, score

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/task_page1.html', methods=['GET', 'POST'])
def task_tracker():
    password_message = ""
    completed_tasks = session.get('completed_tasks', [])
    progress = session.get('progress', 0)
    score = session.get('score', 0)

    if request.method == 'POST':
        if 'verify' in request.form and request.form['verify'] == 'true':
            password = request.form.get('password')
            if password == correct_password:
                session['verified'] = True
                password_message = "Password is correct!"
            else:
                password_message = "Incorrect password. Please try again."
        elif 'complete' in request.form:
            if session.get('verified'):
                if 'tasks' in request.form:
                    completed_tasks = request.form.getlist('tasks')
                    session['completed_tasks'] = completed_tasks
                progress, score = calculate_progress(completed_tasks)
                session['progress'] = progress
                session['score'] = score
                password_message = "Tasks updated successfully!"
            else:
                password_message = "Please verify password first."
        elif 'exit' in request.form:
            session['verified'] = False
            password_message = "Tasks locked."

    return render_template(
        'task_page1.html',
        tasks=tasks,
        completed_tasks=session.get('completed_tasks', []),
        progress=session.get('progress', 0),
        score=session.get('score', 0),
        password_message=password_message
    )

if __name__ == '__main__':
    app.run(debug=True)
