# Imports
import math
import numpy as np
from numpy import arctan2,random,sin,cos,degrees
import pyproj

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
    if bearing + 0.01 > 360:
        return 0
    else:
        return round(bearing + 0.01,2)

def turn_left(bearing):
    if bearing == 0:
        return 360
    else:
        return round(bearing - 0.01,2)

# Get robot current location nad direction
robot_coord = (39.099912,-94.581213)
robot_direction = 0

# Get Market Location
marker_coord = (38.627089, -90.200203)
marker_direction = 0

# Calculate bearing from robot to marker
print("Own calculation",get_bearing(robot_coord[0],robot_coord[1],marker_coord[0],marker_coord[1]))
marker_direction = get_bearing(robot_coord[0],robot_coord[1],marker_coord[0],marker_coord[1])

while robot_direction != marker_direction:
    if marker_direction <= 180:
        robot_direction = turn_right(robot_direction) 
        print(robot_direction)
    else:
        robot_direction = turn_left(robot_direction) 
        print(robot_direction)

print("Direction matched!\n",robot_direction)
