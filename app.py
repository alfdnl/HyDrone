from flask import Flask, render_template, request, redirect, jsonify
import HyD
from sensors import Sensor as s
import os
from pykml import parser

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["map_UPLOADS"] = os.path.join(APP_ROOT,"map")
p = HyD.HyDrone("awwa234.ddns.net", 51234)
kml = ""

def getcoordinatesfromKML(path_to_kml):
    '''
    Parsing KML coordinates into long and lat
    Return the coordinates for longitude and latitude
    '''
    
    with open(path_to_kml) as f:
        doc = parser.parse(f)

    root = doc.getroot()

    list_of_coor = root.Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text.replace('0 ','').split(',')

    # Remove Unwanted data
    for i in list_of_coor:
        if i == '0':
            print(i)
            list_of_coor.remove(i)

    lon_coor=[]
    lat_coor=[]
    for i in range(len(list_of_coor)):
        if i%2==0:
            print("long : ",list_of_coor[i])
            lon_coor.append(float(list_of_coor[i]))

        else:
            print("lat : ",list_of_coor[i])
            lat_coor.append(float(list_of_coor[i]))
    return lon_coor,lat_coor

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
    p.moveLeft("1000")
    return ("nothing")

@app.route('/right')
def right():
    print("Move right")
    p.moveRight("1000")
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



@app.route("/upload-map", methods=["GET", "POST"])
def upload_map():
    global kml
    if request.method == "POST":

        if request.files:

            map = request.files["map"]

            map.save(os.path.join(app.config["map_UPLOADS"], map.filename))

            print("map saved")
            print(getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"], map.filename)))
            kml = getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"], map.filename))
            return redirect(request.url)

    return render_template("app.html")

@app.route("/kml", methods=["GET", "POST"])
def kml_run():
    print("print kml")
    print(kml)
    return ("nothing")

@app.route('/updateData', methods=['POST'])
def updateData():
    us1 = p.getSensorData(s.ULTRASONIC1)[1]
    us2 = p.getSensorData(s.ULTRASONIC2)[1]
    us3 = p.getSensorData(s.ULTRASONIC3)[1]
    us4 = p.getSensorData(s.ULTRASONIC4)[1]
    pitch = p.getSensorData(s.IMU_PITCH)[1]
    roll = p.getSensorData(s.IMU_ROLL)[1]
    yaw = p.getSensorData(s.IMU_YAW)[1]
    bearing = p.getSensorData(s.COMPASS_BEARING)[1]
    batt_1 = p.getSensorData(s.BATTERY1_VOLTAGE)[1]
    batt_2 = p.getSensorData(s.BATTERY2_VOLTAGE)[1]
    return jsonify(us1, us2 , us3,us4, pitch, roll, yaw, bearing, batt_1, batt_2)

if __name__ == ' __main__':
    app.debug = True
    app.run()