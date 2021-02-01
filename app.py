from flask import Flask, render_template, request, redirect, jsonify
from flask import flash
import HyD
from sensors import Sensor as s
import os
from pykml import parser
import generate_map as gm
import folium
import time
from folium.features import DivIcon
import genetic_algorithm_TSP as GA
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["map_UPLOADS"] = os.path.join(APP_ROOT,"map")
app.secret_key = os.urandom(24)
p = HyD.HyDrone("100.96.1.19", 51234)
filename = ""
speed = "1400"
duration = 1


def getcoordinatesfromKML(path_to_kml):
    '''
    Parsing KML coordinates into long and lat
    Return the coordinates for longitude and latitude
    '''
    
    with open(path_to_kml) as f:
        doc = parser.parse(f)

    root = doc.getroot()

    list_of_coor = root.Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text.replace(" ",',').split(',')
    # print( root.Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text.replace(" ",','))
    print(list_of_coor)
    lon_coor=[]
    lat_coor=[]

    # Remove Unwanted data
    count = 0
    for i in list_of_coor:
        
        print(count)
        if count == 0:
            print("long : ",i)
            lon_coor.append(float(i))
            count += 1
            continue
        if count == 1:
            print("lat : ",i)
            lat_coor.append(float(i))
            count+=1
            continue
        if count == 2:
            print("alt : ",i)
            count = 0
            continue
        

        # if i == '0':
        #     print(i)
        #     list_of_coor.remove(i)

    
    # for i in range(len(list_of_coor)):
    #     if i%2==0:
    #         print("long : ",list_of_coor[i])
    #         lon_coor.append(float(list_of_coor[i]))

    #     else:
    #         print("lat : ",list_of_coor[i])
            # lat_coor.append(float(list_of_coor[i]))
    return lon_coor,lat_coor

@app.route('/')
def main():
    return render_template('app.html')


@app.route('/start')
def start():
    p.connectToRobot()
    time.sleep(1)
    print("Start Motor")
    p.startMotors()
    return ("nothing")

@app.route('/find_south')
def move_to():
    dirc = 180
    movTime = 1
    time.sleep(movTime)
    s = p.sendMessage("GET,ALIM")
    if ("None" not in s):
        robot_bearing = float(s.split(',')[0].split('(')[1])
    while not (robot_bearing<dirc+20 and robot_bearing>dirc+20):
        print("Current Direction: ", robot_bearing)

        if robot_bearing > dirc:
            print("Move Left")
            time.sleep(movTime)
            p.sendMessage("CONTROL,MOVE_LEF1,1200")
            time.sleep(2)
        
        elif robot_bearing < dirc:
            print("Move Right")
            time.sleep(movTime)
            p.sendMessage("CONTROL,MOVE_RIGH1,1200")
        
        time.sleep(movTime)
        s = p.sendMessage("GET,ALIM")
        if ("None" not in s):
            time.sleep(movTime)
            robot_bearing = float(s.split(',')[0].split('(')[1])
        time.sleep(movTime)
    print("Now at Facing South")
    return ("nothing")

@app.route('/find_north')
def find_north():
    dirc = 0
    movTime = 0.2
    s = p.sendMessage("GET,ALIM")
    if ("None" not in s):
        robot_bearing = float(s.split(',')[0].split('(')[1])

    while robot_bearing<dirc+20 and robot_bearing>dirc+20:
        if robot_bearing > dirc:
            time.sleep(0.2)
            p.sendMessage("CONTROL,MOVE_LEF1,1200")
            time.sleep(movTime)
            p.moveForward("1000","1000")
        elif robot_bearing > dirc:
            time.sleep(0.2)
            p.sendMessage("CONTROL,MOVE_RIGH1,1200")
            time.sleep(movTime)
            p.moveForward("1000","1000")
        s = p.sendMessage("GET,ALIM")
        if ("None" not in s):
            robot_bearing = float(s.split(',')[0].split('(')[1])
    print("Now at Facing North")        
    return ("nothing")


@app.route('/left')
def left():
    print("Move left")
    # p.sendMessage("CONTROL,MOVE_LEF1,1200")
    p.moveLeft("1200")
    time.sleep(duration)
    p.moveForward("1000","1000")
    #p.moveLeft("1200")
    return ("nothing")

@app.route('/right')
def right():
    print("Move right")
    # p.sendMessage("CONTROL,MOVE_RIGH1,1200")
    p.moveRight("1200")
    time.sleep(duration)
    p.moveForward("1000","1000")
    #p.moveRight("1200")
    return ("nothing")

@app.route('/stopMoving')
def stopMoving():
    print("stop moving")
    p.moveForward("1000","1000")
    return ("nothing")

@app.route('/stop')
def stop():
    print("Stop motor")
    p.stopMotors()
    
    time.sleep(2)
    p.disconnectWithRobot()

    return ("nothing")

@app.route('/forward')
def forward():
    print("move forward")
    p.moveForward(speed,speed)
    # p.moveBackward("1300","1300")
    time.sleep(duration)
    p.moveForward("1000","1000")
    return ("nothing")

@app.route('/backward')
def backward():
    print("move backward")
    p.moveBackward("1200","1200")
    time.sleep(2)
    p.moveBackward("1000","1000")
    return ("nothing")

@app.route('/sample')
def sample():
    print("Take water sample")
    p.collectWaterSample("1")
    return ("nothing")



@app.route("/", methods=["GET", "POST"])
def upload_map():

    ## If map2 exist: remove
    if 'map2.html' in os.listdir('templates'):
        print("exist")
        os.remove("templates/map2.html")
        

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
        if filename.split(".")[-1]!='kml':
            print("Not KMl")
            data=[]
            polygon=[]
            flash("File type is not kml. Please upload KML file.")

        
        else:
            ## Get coordinates
            lon,lat = getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"],filename))
            print(lon,lat)
            ## Get Polygon
            poly,_ = gm.getpolygon(lon,lat)
            print(poly)

            ## split lake
            global lake_size 
            lake_size = float(request.form["slider"])
            print("Lake Size: ", lake_size)
            test2 = gm.split_lake(poly,1e-04 * (lake_size))
            

            ## get map with robot online
            # allData = p.getSensorData(s.ALL_DATA)
            # c_lat = allData[8].split(":")[1]
            # c_lon = allData[9].split(":")[1]
            # m = gm.printMap([c_lat,c_lon],100,poly)

            ## Get map with robot offline
            # m = gm.printMap([3.1189078118594447,101.65878139637647],100,poly)

            # ## Add marker
            # for idx,i in enumerate(test2):
            #     folium.GeoJson(i).add_to(m)
            #     folium.Marker([i.centroid.y, i.centroid.x]).add_to(m)
            #     folium.Marker([i.centroid.y,i.centroid.x], icon=DivIcon(
            #         icon_size=(10,10),
            #         icon_anchor=(4,63),
            #         html='<div style="font-size: 14pt; color : red">{}</div>'.format(idx),
            #         )).add_to(m)
            #     m.save('templates/map.html')
            print("Done")


            data = []
            for idx,i in enumerate(test2):
                data.append((i.centroid.y, i.centroid.x))

            polygon = []
            for i in test2:
                polygon.append({
                                "longitude":i.exterior.coords.xy[0].tolist()
                                ,"latitude":i.exterior.coords.xy[1].tolist()})
                print(type(i.exterior.coords.xy))
                print(i.exterior.coords.xy[0].tolist())
                print(i.exterior.coords.xy[1].tolist())
            

    # polygon = [1, 'foo']
    

    return render_template("app.html", data = data, polygon=polygon)

@app.route("/kml", methods=["GET", "POST"])
def kml_run():
     if request.method == "POST":
        if filename == "" or filename.split(".")[-1]!='kml':
            marker=[]
            bestpath=[]
            flash("Kml file not found. Please upload KML file.")

        else:
            # print(request.form["slider"])
            ## Get coordinates
            lon,lat = gm.getcoordinatesfromKML(os.path.join(app.config["map_UPLOADS"],filename))

            ## Get Polygon
            poly,_ = gm.getpolygon(lon,lat)
            
            ## split lake
            test2 = gm.split_lake(poly,1e-04 * (lake_size))
            print(test2)

            ## get the coordinates of the centroids
            markers = []
            for idx,i in enumerate(test2):
                    print((i.centroid.y, i.centroid.x))
                    markers.append((i.centroid.y, i.centroid.x))

            ## GEt current coordinates of robot
            # This coordinate will also be included in Genetic Algorithm #
            # this will be the home coordinate
            # allData = p.getSensorData(s.ALL_DATA)
            # lat = float(allData[8].split(":")[1])
            # lon = float(allData[9].split(":")[1])
            # home = (lat, lon) # Change back later
            home = (3.119629449776096, 101.65642710502878)
            # print(home)

            ## Initiate the marker class
            markersList = []
            markersList.append(GA.Marker(x=home[0], y=home[1]))
            for i in range(len(markers)):
                markersList.append(GA.Marker(x=markers[i][0], y=markers[i][1]))

            home = markersList[0]

            ## Marker mapping
            mapping_dict = {}
            for idx, i in enumerate(markersList):
                mapping_dict[i] = idx

            print(mapping_dict)

            bestpath = GA.geneticAlgorithm(population=markersList,home=home, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
            marker = []

            for idx,i in enumerate(bestpath):
                # bestroute.append(mapping_dict[i])
                print(mapping_dict[i])
                marker.append(mapping_dict[i])

            print(marker)
            print(bestpath)

            # m = folium.Map([3.1189078118594447,101.65878139637647], zoom_start=100, tiles='cartodbpositron')
            # ## Add marker
            # for idx,i in enumerate(bestpath):
            #     print(mapping_dict[i])
            #     folium.Marker([i.x,i.y]).add_to(m)
            #     folium.Marker([i.x,i.y], icon=DivIcon(
            #         icon_size=(10,10),
            #         icon_anchor=(4,63),
            #         html='<div style="font-size: 14pt; color : red">{}</div>'.format(idx),
            #         )).add_to(m)
            #     m.save('templates/map2.html')
            print("Done")
        return render_template("app.html", marker = marker, bestpath = bestpath ,  polygon = [0])

# @app.route('/map',  methods=["GET", "POST"])
# def map():
#     if 'map.html' not in os.listdir('templates'):
#         print("no map")

#         # Connected to robot
#         allData = p.getSensorData(s.ALL_DATA)
#         lat = allData[8].split(":")[1]
#         lon = allData[9].split(":")[1]        
#         m = folium.Map([lat,lon], zoom_start=100, tiles='cartodbpositron')
#         folium.Marker([lat, lon],color = 'black').add_to(m)

#         # Not connected to robot
#         # m = folium.Map([3.1189078118594447,101.65878139637647], zoom_start=100, tiles='cartodbpositron')
#         # folium.CircleMarker([3.1189078118594447, 101.65878139637647],color = 'red',fill_color='red').add_to(m)
#         return m._repr_html_()

#     elif 'map2.html' in os.listdir('templates'):
#         return render_template('map2.html')

#     else:
#         return render_template('map.html')

@app.route('/get_location', methods=['POST','GET'])
def updateLocation():

    allData = p.getSensorData(s.ALL_DATA)
    lat = float(allData[8].split(":")[1])
    lon = float(allData[9].split(":")[1])
    # print(allData)
    return jsonify(lat, lon)

@app.route('/updateData', methods=['POST'])
def updateData():

    allData = p.getSensorData(s.ALL_DATA)
    if len(allData)>12:
        us1 = allData[0].split(":")[1]
        us2 = allData[1].split(":")[1]
        us3 = allData[2].split(":")[1]
        us4 = allData[3].split(":")[1]
        pitch = allData[4].split(":")[1]
        roll = allData[5].split(":")[1]
        yaw = allData[6].split(":")[1]
        bearing = allData[14].split(":")[1]
        batt_1 = allData[12].split(":")[1]
        batt_2 = allData[13].split(":")[1]
        return jsonify(us1, us2 , us3,us4, pitch, roll, yaw, bearing, batt_1, batt_2)

if __name__ == ' __main__':
    
    app.debug = True
    app.run()