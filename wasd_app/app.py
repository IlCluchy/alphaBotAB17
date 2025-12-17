from flask import Flask, render_template, request
from libreries.AlphaBot import AlphaBot

app = Flask(__name__)

robot = None

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
        
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        command = request.form.get("cmd")
        handle_command(command)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
