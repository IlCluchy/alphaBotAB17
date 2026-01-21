import sqlite3
import hashlib
import binascii
from flask import Flask, render_template, request
from libreries.AlphaBot import AlphaBot

app = Flask(__name__)

DB_NAME = "alphaBotDB.db"
ITERATIONS = 200_000

robot = None

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

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return verify_password(password, row[0])
    return False

# -------------------
#       LOGIN
# -------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if authenticate_user(username, password):
            return render_template("command.html")
        else:
            return render_template("index.html", error="Invalid credentials")

    return render_template("index.html")


@app.route("/command", methods=["POST"])
def command():
    cmd = request.form.get("cmd")
    handle_command(cmd)
    return render_template("command.html")

# -------------------
#       MAIN
# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=False, processes=1)
