from flask import Flask, request,render_template, redirect,session, request, jsonify, url_for 
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
# Pomodoro
import time
import threading
import os
import pygame
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return render_template('index.html')


# Calendar

events = [
    {
        'title': 'TestEvent',
        'start': '2023-12-17',
        'end': '',
        'url' : 'https://youtube.com'
    },
    {
        'title': 'Another TestEvent',
        'start': '2023-12-18',
        'end': '2023-12-19',
        'url' : 'https://google.com'
    }
]

@app.route('/calendar')
def calendar():
    
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('calendar.html',user=user, events=events)
   


@app.route('/add_event',methods=['GET',"POST"])
def add_event():
    if request.method == "POST":
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end' : end,
            'url' : url
        },
        )
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('add.html',user=user)
  

@app.route('/event/<int:event_id>')
def view_event(event_id):
    event = events[event_id]
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('event.html',user=user, event=event)
    

# Attendance Calculator
@app.route('/attendance')
def attendance():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('attendance.html',user=user)
    

@app.route('/calculate_attendance', methods=['POST'])
def calculate_attendance():
    try:
        total_subjects = 5
        total_classes = [int(request.form[f'total_classes_{i}']) for i in range(total_subjects)]
        classes_attended = [int(request.form[f'classes_attended_{i}']) for i in range(total_subjects)]

        attendance_percentage = [(attended / total) * 100 for total, attended in zip(total_classes, classes_attended)]

        status = ["Good" if percent >= 75 else "Low" for percent in attendance_percentage]

        result = {
            f"Subject {i + 1}": {
                'attendance_percentage': percentage,
                'status': stat
            } for i, (percentage, stat) in enumerate(zip(attendance_percentage, status))
        }

        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Please enter valid numeric values for total classes and classes attended.'})

# CGPA Calculator
@app.route('/cgpa')
def cgpa():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('cgpa.html',user=user)

@app.route('/calculate_cgpa', methods=['POST'])
def calculate_cgpa():
    try:
        total_credits = 0
        total_grade_points = 0

        for i in range(1, 6):  # Fixed number of subjects (5)
            gained_credits = int(request.form[f'gained_credits_{i}'])
            total_credits_subject = int(request.form[f'total_credits_{i}'])
            grade = request.form[f'grade_{i}'].upper()

            grade_points = 0
            if grade == 'A':
                grade_points = 4.0
            elif grade == 'B':
                grade_points = 3.0
            elif grade == 'C':
                grade_points = 2.0
            elif grade == 'D':
                grade_points = 1.0

            total_credits += gained_credits
            total_grade_points += gained_credits * grade_points / total_credits_subject

        cgpa = total_grade_points / total_credits
        result = {'cgpa': cgpa}

        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Please enter valid numeric values for gained credits, total credits, and total subjects.'})  

#Pomodoro

socketio = SocketIO(app)

# Event to control pausing and resuming the timer
pause_event = threading.Event()
stop_event = threading.Event()

# Pomodoro timer variables
work_time = 25
break_time = 5
long_break_time = 15
rounds_before_long_break = 4
total_rounds = float('inf')


# Function to play sound
def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Route for the home page

@app.route('/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')


# Route to FormSubRoute
@app.route('/FormSubRoute', methods=['POST'])
def FormSubRoute():
    if request.form['submitaction']=="StartTimer":
        stop_event.clear()
        start_timer()
    return "Submitted!"

# Route to start the Pomodoro timer
@app.route('/start_timer', methods=['POST'])
def start_timer():
    global work_time, break_time, long_break_time, rounds_before_long_break, total_rounds
    
    work_time = int(request.form['work_time'])
    break_time = int(request.form['break_time'])
    long_break_time = int(request.form['long_break_time'])
    rounds_before_long_break = int(request.form['rounds_before_long_break'])
    total_hours_input = request.form['total_hours']
    
    if total_hours_input:
        total_hours = float(total_hours_input)
        total_minutes = total_hours * 60
        total_rounds = total_minutes // (work_time + (break_time * rounds_before_long_break))

    # Start the Pomodoro timer in a new thread
    threading.Thread(target=pomodoro_timer_dynamic).start()

    return "Timer started!"

# Variable to store the remaining time dynamically
remaining_time = 0

# Function to run the Pomodoro timer with dynamic countdown
def pomodoro_timer_dynamic():
    global work_time, break_time, long_break_time, rounds_before_long_break, total_rounds, remaining_time

    round_number = 0
    while total_rounds == float('inf') or round_number < total_rounds:
        if stop_event.is_set():
            stop_event.clear()
            pause_event.clear()
            return
            break


        round_number += 1

        # Work time
        remaining_time = work_time * 60
        while remaining_time > 0:
            if stop_event.is_set():
                stop_event.clear()
                pause_event.clear()
                return
                break
            if not pause_event.is_set():
                time.sleep(1)
                remaining_time -= 1

        # Play work complete sound
        play_sound('bell-172780.mp3')
        play_sound('bell-172780.mp3')

        # Check if it's time for a long break
        if round_number % rounds_before_long_break == 0 and round_number != total_rounds:
            remaining_time = long_break_time * 60
            while remaining_time > 0:
                if stop_event.is_set():
                    stop_event.clear()
                    pause_event.clear()
                    return
                    break
                if not pause_event.is_set():
                    time.sleep(1)
                    remaining_time -= 1

            # Play long break complete sound
            play_sound('bright-ringtone-loop-151768.mp3')
        else:
            # Regular break time
            remaining_time = break_time * 60
            while remaining_time > 0:
                if stop_event.is_set():
                    stop_event.clear()
                    pause_event.clear()
                    return
                    break
                if not pause_event.is_set():
                    time.sleep(1)
                    remaining_time -= 1

            # Play break complete sound
            play_sound('notification-interface-success-positive-corrects-132471.mp3')
            play_sound('notification-interface-success-positive-corrects-132471.mp3')
            play_sound('notification-interface-success-positive-corrects-132471.mp3')

# Route to get the remaining countdown dynamically
@app.route('/get_countdown', methods=['GET'])
def get_countdown():
    global remaining_time
    return str(remaining_time)

# Route to pause the Pomodoro timer
@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    # print("Stop: "+str(stop_event.is_set()));
    stop_event.set()
    # print("Stop: "+str(stop_event.is_set()));
    return "Timer Stopped!"

# Route to pause the Pomodoro timer
@app.route('/pause_timer', methods=['POST'])
def pause_timer():
    # print(pause_event.is_set());
    pause_event.set()
    # print(pause_event.is_set());
    return "Timer paused!"

# Route to resume the Pomodoro timer
@app.route('/resume_timer', methods=['POST'])
def resume_timer():
    # print(pause_event.is_set());
    pause_event.clear()
    # print(pause_event.is_set());
    return "Timer resumed!"



# To-Do

try:
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []


def save_tasks():
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)


@app.route('/todo')
def todo():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('todo.html',user=user, tasks=tasks, enumerate=enumerate)


@app.route('/todoadd', methods=['POST'])
def todoadd():
    task_name = request.form.get('task')
    new_task = {'name': task_name, 'complete': False}
    tasks.append(new_task)
    save_tasks()
    return redirect(url_for('todo'))


@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['complete'] = not tasks[task_id]['complete']
        save_tasks()
    return redirect(url_for('todo'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
        save_tasks()
    return redirect(url_for('todo'))

@app.route('/profile')
def profile():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('profile.html',user=user)
    
#Note-taking
    
notes = []

@app.route('/notes')
def notes():
    load_notes() # Load notes from file
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('notes.html',user=user, notes=notes)


@app.route('/add_note', methods=['POST'])
def add_note():
    # Get the note text and color from the form submission
    note_text = request.form['note_text']
    note_color = request.form['note_color']
    # Add the note to the list of notes
    notes.append({'text': note_text, 'color': note_color})
    save_notes() # Save notes to file
    return redirect(url_for('notes'))
    #return notes()

@app.route('/delete_note/<int:note_id>', methods=['GET', 'POST'])
def delete_note(note_id):
    if request.method == 'POST':
        # Delete the note with the given ID from the list of notes
        del notes[note_id]
        save_notes() # Save notes to file
    return redirect(url_for('notes'))
    # Return the updated index page
    #return notes()

def load_notes():
    global notes
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []

def save_notes():
    with open('notes.json', 'w') as file:
        json.dump(notes, file, indent=4)

    
if __name__ == '__main__':
    app.run(debug=True)