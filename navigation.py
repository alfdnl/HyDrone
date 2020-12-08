# Imports
import math
import numpy as np
from numpy import arctan2,random,sin,cos,degrees
import pyproj
import HyD
from sensors import Sensor as s
p = HyD.HyDrone("100.96.1.19", 51234)


## TO-Do
# 1. Make the codes runs in the loop
# 2. Use the real data set
# 3. Make the code uses the real function to move the robot.
# 4. Make a function to check wheter it has arrived to the next marker
# 5. Make the robot move continously until it reached back to it current position.

geodesic = pyproj.Geod(ellps='WGS84')

# Functions
def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = arctan2(x,y)
    brng = degrees(brng)
    return round(brng,2)

def turn_right(bearing):
    print("Move right")
    p.moveRight("1200")

def turn_left(bearing):
    print("Move left")
    p.moveLeft("1200")

def move_forward():
    return

# Get robot current location and direction
# allData = p.getSensorData(s.ALL_DATA)
# lat = float(allData[8].split(":")[1])
# lon = float(allData[9].split(":")[1])
# current_location = (lat,lon)
# robot_bearing = float(allData[14].split(":")[1])
current_location = (3.119629449776096, 101.65642710502878)
robot_bearing = 0

# Get Market Location
## the long one will be added later
markers = [(3.119629449776096, 101.65642710502878),
(3.119570613676185, 101.65657144167113),
(3.11950698203576, 101.65672277258696),
(3.119450850925013, 101.65687356698822),
(3.1194002523972264, 101.65702708276075),
(3.1193620989000945, 101.65717911039806),
(3.119237741578333, 101.65733614239487),
(3.119210480539193, 101.65748546964066),
(3.1193747311242292, 101.65732762732425),
(3.1193651207520348, 101.65747932987146),
(3.1191452863986697, 101.6576379980372),
(3.119117835549454, 101.6577883650018),
(3.119318123645613, 101.65763163276269),
(3.1193085095435045, 101.65778339418767),
(3.1190526841770363, 101.65794065912831),
(3.119025140123476, 101.65809153663653),
(3.1192615207635943, 101.65793556564249),
(3.119251904521294, 101.65808736085103),
(3.118962905339048, 101.65824361260565),
(3.1189384653502845, 101.65839337817877),
(3.119207798610268, 101.65823943589713),
(3.1191981812041214, 101.65839124947732),
(3.11899320291459, 101.65852313161388),
(3.119190524651296, 101.65854303493941),
(3.1192110057350386, 101.65867096627734)
]


visited_node = []
print("Own calculation",get_bearing(current_location[0],current_location[1],markers[1][0],markers[1][1]))
for marker in markers:

    # Get current location

    # Calculate bearing from robot to marker
    marker_direction = get_bearing(current_location[0],current_location[1],marker[0],marker[1])
    print("Own calculation",get_bearing(current_location[0],current_location[1],marker[0],marker[1]))
    while current_location != marker:
        while robot_direction != marker_direction:
            if marker_direction  <= 180:
                while
                turn_right(robot_direction) 
            else:
                turn_left()
        
        for _ in range(5):
            move_forward()
            time.sleep(0.02)
    visited_node.append(marker)
    current_location = marker
        


marker_direction = get_bearing(robot_coord[0],robot_coord[1],marker_coord[0],marker_coord[1])

while robot_direction != marker_direction:
    if marker_direction <= 180:
        robot_direction = turn_right(robot_direction) 
        print(robot_direction)
    else:
        robot_direction = turn_left(robot_direction) 
        print(robot_direction)

print("Direction matched!\n",robot_direction)
# Move for 5 secs and repeat until target reached

# To check that the robot is at the marker
# calculate the distance between the marker and the robot
# If the distance is less than a meter, check as visited.
