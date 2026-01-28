import sqlite3
import hashlib
import binascii
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from libreries.AlphaBot import AlphaBot
from libreries.movement import circle, triangle, square

app = Flask(__name__)
app.secret_key = 'chiave-sicura'

DB_NAME = "alphaBotDB.db"
ITERATIONS = 200_000

robot = None

# -------------------
# FLASK-LOGIN SETUP
# -------------------
login_manager = LoginManager()
login_manager.init_app(app) #collega il login manager all'app flask
login_manager.login_view = 'login' #reindirizza uno user non autenticato alla pagina di login

class User(UserMixin):   #UserMinxin inizializza le funzioni fondamentali di flask-login
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader # user_loader ricarica l'utente dalla sessione
def load_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(row[0], row[1])
    return None

# ---------------------
# FLASK-LOGIN FUNCTION
# ---------------------

def verify_user_data(username, password):
    user_data = get_user_by_username(username)
        
    if user_data and verify_password(password, user_data[2]):
        user = User(user_data[0], user_data[1])
        login_user(user)

        session['username'] = user.username
        session['user_id'] = user.id
        session['robot_status'] = 'stopped'
        session['last_command'] = None

        return redirect('command')
    else:
        flash("Credenziali non valide. Riprova.", "error")
        return None

# -------------------
# ROBOT FUNCTIONS
# -------------------
def get_robot():
    global robot
    if robot is None:
        robot = AlphaBot()
        robot.stop()
    return robot

def handle_command(command):
    r = get_robot()
    if command == 'w':
        r.stop()
        r.forward()
    elif command == 'a':
        r.stop()
        r.left()
    elif command == 'd':
        r.stop()
        r.right()
    elif command == 's':
        r.stop()
        r.backward()
    elif command == 'stop':
        r.stop()
    elif get_movement(command) == "circle":
        r.stop()
        circle(r, "right", 30, 1)
        r.stop()
    elif get_movement(command) == "square":
        r.stop()
        #robot, direction, speed, forward_time, turn_delay
        square(r, "right", 30, 1,0.3)
        r.stop()
    elif get_movement(command) == "triangle":
        r.stop()
        triangle(r, "right", 30, 1,0.3)
        r.stop()
    
    
    session['last_command'] = command
    session['robot_status'] = 'moving' if command != 'stop' else 'stopped'

# -------------------
# DB FUNCTIONS
# -------------------
def verify_password(password: str, stored_hash: str) -> bool:
    try:
        method, iterations, data = stored_hash.split('$')
        iterations = int(iterations)
        data = binascii.unhexlify(data)
        salt = data[:16]
        stored_key = data[16:]
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
        return new_key == stored_key
    except:
        return False

def get_user_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_movement(command):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name_function FROM movements WHERE command = ?", (command,))
    row = cursor.fetchone()
    conn.close()
    print(row)
    return row[0]

# -------------------
# ROUTES
# -------------------
@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        result = verify_user_data(username, password)
        if result:
            return result
    
    return render_template("index.html")

@app.route("/command", methods=["GET", "POST"])
@login_required
def command():
    if request.method == "POST":
        cmd = request.form.get("cmd")
        handle_command(cmd)
        return redirect(url_for('command'))
    
    last_cmd = session.get('last_command', 'Nessun comando ancora')
    robot_status = session.get('robot_status', 'stopped')

    return render_template("command.html", username=current_user.username, last_command=last_cmd, robot_status=robot_status)

@app.route("/logout")
@login_required
def logout():
    if robot is not None:
        robot.stop()
    
    logout_user()
    session.clear()
    flash("Logout effettuato con successo.", "success")
    return redirect(url_for('login'))

# -------------------
# MAIN
# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)