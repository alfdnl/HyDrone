from flask import Flask, render_template, request, redirect
import HyD
from sensors import Sensor
import os
from pykml import parser

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["IMAGE_UPLOADS"] = os.path.join(APP_ROOT,"map")
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



@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    global kml
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            print("map saved")
            print(getcoordinatesfromKML(os.path.join(app.config["IMAGE_UPLOADS"], image.filename)))
            kml = getcoordinatesfromKML(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return redirect(request.url)

    return render_template("app.html")

@app.route("/kml", methods=["GET", "POST"])
def kml_run():
    print("print kml")
    print(kml)
    return ("nothing")

if __name__ == ' __main__':
    app.debug = True
    app.run()