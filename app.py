from flask import Flask, render_template, request
import HyD
from sensors import Sensor

app = Flask(__name__)
p = HyD.HyDrone("awwa234.ddns.net", 51234)

@app.route('/')
def main():
    return render_template('app.html')


@app.route('/start')
def start():
    print("Start Motor")
    p.startMotors()
    return ("nothing")

@app.route('/left')
def left():
    print("Move left")
    p.moveLeft("1500")
    return ("nothing")

@app.route('/right')
def right():
    print("Move right")
    p.moveRight("1500")
    return ("nothing")

@app.route('/stop')
def stop():
    print("Stop motor")
    p.stopMotors()
    return ("nothing")

@app.route('/sample')
def sample():
    print("Take water sample")
    p.collectWaterSample("1")
    return ("nothing")

if __name__ == ' __main__':
    app.debug = True
    app.run()