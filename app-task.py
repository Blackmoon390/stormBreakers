from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "secret_key"  # Important: Change this to a random, secure key

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

@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)