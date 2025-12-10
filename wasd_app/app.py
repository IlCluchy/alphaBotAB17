from flask import Flask, render_template, request
from libreries.AlphaBot2 import AlphaBot
from libreries import movement

app = Flask(__name__)

robot = AlphaBot()
robot.stop()

#Pagina 1 --> form per inviare dati
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        comando = request.form.get("cmd")
        
    if comando == 'w':
        robot.stop()
        robot.forward()
    elif comando == 'a':
        robot.stop()
        robot.left()
    elif comando == 'd':
        robot.stop()
        robot.right()
    elif comando == 's':
        robot.stop()
        robot.backward()
    elif comando == 'stop':
        robot.stop()
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
