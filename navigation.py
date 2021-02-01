# Imports
import math
import numpy as np
from numpy import arctan2,random,sin,cos,degrees
import pyproj
import time
import HyD
from sensors import Sensor as s

from math import radians, cos, sin, asin, sqrt
p = HyD.HyDrone("100.96.1.19", 51234)

geodesic = pyproj.Geod(ellps='WGS84')

# Functions
def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = arctan2(x,y)
    brng = degrees(brng)
    compass_bearing = (brng + 360) % 360
    return round(compass_bearing,2)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return round(c * r,4)

def turn_right():
    print("Move right")
    # p.moveRight("1200")
    p.sendMessage("CONTROL,MOVE_RIGH1,1200")
    time.sleep(1)
    p.moveForward("1000","1000")

def turn_left():
    print("Move left")
    # p.moveLeft("1200")
    # time.sleep(1)
    p.sendMessage("CONTROL,MOVE_LEF1,1200")
    time.sleep(1)
    p.moveForward("1000","1000")

def move_forward():
    p.moveForward("1300","1300")
    return

def get_current_bearing():
    while True:
        time.sleep(1)
        try:
            # p.moveLeft("1200")
            s = p.sendMessage("GET,ALIM")
            if ("None" not in s):
                robot_bearing = float(s.split(',')[0].split('(')[1])
                print("robot current bearing: ", robot_bearing)
                return robot_bearing
        except:
             print("data not found")


def get_current_location():
    while True:
        try:
            allData = p.getSensorData(s.ALL_DATA)
            lat = float(allData[8].split(":")[1])
            lon = float(allData[9].split(":")[1])
            current_location = (lat,lon)
            print("robot current location: ", current_location)
            return current_location
        except:
            print("data not found")




# robot offline
# current_location = (3.119629449776096, 101.65642710502878)
# robot_bearing = 0

# Get Market Location
## the long one will be added later
# markers = [(3.119629449776096, 101.65642710502878),
# (3.119570613676185, 101.65657144167113),
# (3.11950698203576, 101.65672277258696),
# (3.119450850925013, 101.65687356698822),
# (3.1194002523972264, 101.65702708276075),
# (3.1193620989000945, 101.65717911039806),
# (3.119237741578333, 101.65733614239487),
# (3.119210480539193, 101.65748546964066),
# (3.1193747311242292, 101.65732762732425),
# (3.1193651207520348, 101.65747932987146),
# (3.1191452863986697, 101.6576379980372),
# (3.119117835549454, 101.6577883650018),
# (3.119318123645613, 101.65763163276269),
# (3.1193085095435045, 101.65778339418767),
# (3.1190526841770363, 101.65794065912831),
# (3.119025140123476, 101.65809153663653),
# (3.1192615207635943, 101.65793556564249),
# (3.119251904521294, 101.65808736085103),
# (3.118962905339048, 101.65824361260565),
# (3.1189384653502845, 101.65839337817877),
# (3.119207798610268, 101.65823943589713),
# (3.1191981812041214, 101.65839124947732),
# (3.11899320291459, 101.65852313161388),
# (3.119190524651296, 101.65854303493941),
# (3.1192110057350386, 101.65867096627734)
# ]

## Dummy marker to test
markers = [(3.1191, 101.658) # the center of the lake from kayak place
]

p.connectToRobot()
time.sleep(2)
p.startMotors()
time.sleep(3)
###
# To Test: 
## Can the robot turn until its current bearing == to the bearing calculated
## Put the robot at the kayak place and face other direction. not towards the marker.


visited_node = []
# print("Own calculation",get_bearing(current_location[0],current_location[1],markers[1][0],markers[1][1]))
for marker in markers:
    print(marker)

    # Get current location
    # Get robot current location and direction   
    current_location = get_current_location()
    robot_bearing = get_current_bearing()
    

    # Calculate bearing from robot to marker
    marker_direction = get_bearing(current_location[0],current_location[1],marker[0],marker[1])
    # marker_direction = abs(marker_direction)
    print("Bearing to marker from robot: ", marker_direction)

    # Calculate distance between marker and current location
    # While the distance is not less than 5 meter, move

    # calculate distance to marker
    distance_to_marker = haversine(current_location[1],current_location[0],marker[1],marker[0])
    # print(distance_to_marker)

    while distance_to_marker > 0.001:
        print("Current distance to maker: ",distance_to_marker)
        while abs(robot_bearing - marker_direction) > 30:
            
            print(marker_direction - robot_bearing)
            if marker_direction - robot_bearing  >=  0:
                turn_right()
                time.sleep(1)

            else:                
                turn_left()
                time.sleep(1)
            
            robot_bearing = get_current_bearing()
            
        
        print("Direction reached")
        # break
        
        
        move_forward()
        time.sleep(5)
        p.moveForward("1000","1000")

        
        # update new distance
        current_location = get_current_location()
        distance_to_marker = haversine(current_location[1],current_location[0],marker[1],marker[0])

        ## Get current direction
        marker_direction = get_bearing(current_location[0],current_location[1],marker[0],marker[1])
        
    # # visited_node.append(marker)
    current_location = marker
    print("Marker Reached")
p.stopMotors()

time.sleep(2)

p.disconnectWithRobot()
print("Goal Achieved")

