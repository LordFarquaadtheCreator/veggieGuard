from operator import methodcaller
from flask import session
from flask import request, render_template, Flask, redirect, url_for, make_response, g
from os import urandom
import sqlite3
from pymongo.errors import ConnectionFailure
import os
from helpers import login_required
from flask_session import Session

#account_sid = os.environ['AC8ef87725499512171f849e7a4beb8dc0']

app = Flask(__name__)
debug = True
app.secret_key = urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
DATABASE = 'columbia.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Ensure required fields are filled
        if not request.form.get('email') or not request.form.get('passw') or not request.form.get('first_name') or not request.form.get('last_name'):
            return render_template('error.html')

        email = request.form.get('email')
        passw = request.form.get('passw')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        db = get_db()
        cursor = db.cursor()

        # Check if email already exists in the database
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('error.html')

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (first_name, last_name, email, passw) VALUES (?, ?, ?, ?)',
                       (first_name, last_name, email, passw))
        db.commit()

        # Store user information in the session
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        session['user_id'] = user['id']

        return redirect(url_for('mainpage'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passw = request.form.get('passw')  # Rename to "password" for clarity

        db = get_db()
        cursor = db.cursor()

        # Retrieve the user's record from the database based on email
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if not user:
            return render_template('error.html')

        # Compare the provided password with the password stored in the database
        if user['passw'] != passw:
            return render_template('error.html')

        # Store user information in the session
        session['user_id'] = user['id']
        return redirect(url_for('mainpage'))

    return render_template('login.html')

@app.route('/')
def mainpage():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)