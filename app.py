from flask import Flask, render_template, request, redirect, jsonify
import HyD
from sensors import Sensor as s
import os
from pykml import parser
import generate_map as gm
import folium
import time
from folium.features import DivIcon

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["map_UPLOADS"] = os.path.join(APP_ROOT,"map")
p = HyD.HyDrone("100.19.1.19", 51234)
filename = ""

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
    global filename
    if request.method == "POST":

        if request.files:

            map = request.files["map"]

            map.save(os.path.join(app.config["map_UPLOADS"], map.filename))
            filename = map.filename
            print("map saved")
            # print(getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"], map.filename)))
            # kml = getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"], map.filename))
            # return redirect(request.url)
    
    print("print kml")
    print("Filename: "+ filename)
    ## Get coordinates
    lon,lat = gm.getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"],filename))

    ## Get Polygon
    poly,_ = gm.getpolygon(lon,lat)

    ## split lake
    test2 = gm.split_lake(poly,6e-04)
    

    # c_lat = p.getSensorData(s.GPS_LATITUDE)
    # time.sleep(0.3)
    # c_lon = p.getSensorData(s.GPS_LONGITUDE)
    # time.sleep(0.3)
    # m = gm.printMap([c_lat,c_lon],100,poly)

    ## Get map
    m = gm.printMap([3.1189078118594447,101.65878139637647],100,poly)

    ## Add marker
    for idx,i in enumerate(test2):
        folium.GeoJson(i).add_to(m)
        folium.Marker([i.centroid.y, i.centroid.x]).add_to(m)
        folium.Marker([i.centroid.y,i.centroid.x], icon=DivIcon(
            icon_size=(10,10),
            icon_anchor=(4,63),
            html='<div style="font-size: 14pt; color : red">{}</div>'.format(idx),
            )).add_to(m)
        m.save('templates/map.html')
    print("Done")

    return render_template("app.html")

@app.route("/kml", methods=["GET", "POST"])
def kml_run():    
    return ("nothing")

@app.route('/map')
def map():
    if 'map.html' not in os.listdir('templates'):
        print("no map")
        # Connected to robot
        # lat = p.getSensorData(s.GPS_LATITUDE)
        # time.sleep(0.3)
        # lon = p.getSensorData(s.GPS_LONGITUDE)
        # time.sleep(0.3)
        # m = folium.Map([lat,lon], zoom_start=100, tiles='cartodbpositron')
        # folium.Marker([lat, lon],color = 'black').add_to(m)

        # Not connected to robot
        m = folium.Map([3.1189078118594447,101.65878139637647], zoom_start=100, tiles='cartodbpositron')
        folium.CircleMarker([3.1189078118594447, 101.65878139637647],color = 'red',fill_color='red').add_to(m)
        return m._repr_html_()

    else:
        return render_template('map.html')

@app.route('/updateData', methods=['POST'])
def updateData():
    time.sleep(0.3)
    us1 = p.getSensorData(s.ULTRASONIC1)[1]
    time.sleep(0.3)
    us2 = p.getSensorData(s.ULTRASONIC2)[1]
    time.sleep(0.3)
    us3 = p.getSensorData(s.ULTRASONIC3)[1]
    time.sleep(0.3)
    us4 = p.getSensorData(s.ULTRASONIC4)[1]
    time.sleep(0.3)
    pitch = p.getSensorData(s.IMU_PITCH)[1]
    time.sleep(0.3)
    roll = p.getSensorData(s.IMU_ROLL)[1]
    time.sleep(0.3)
    yaw = p.getSensorData(s.IMU_YAW)[1]
    time.sleep(0.3)
    bearing = p.getSensorData(s.COMPASS_BEARING)[1]
    time.sleep(0.3)
    batt_1 = p.getSensorData(s.BATTERY1_VOLTAGE)[1]
    time.sleep(0.3)
    batt_2 = p.getSensorData(s.BATTERY2_VOLTAGE)[1]
    time.sleep(0.3)
    return jsonify(us1, us2 , us3,us4, pitch, roll, yaw, bearing, batt_1, batt_2)

if __name__ == ' __main__':
    app.debug = True
    app.run(host='0.0.0.0')