import HyD
from sensors import Sensor as s
import os
from pykml import parser
import generate_map as gm
import folium
import time
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import genetic_algorithm_TSP as GA

## Get coordinates
lon,lat = gm.getcoordinatesfromKML("map\\test.kml")

## Get Polygon
poly,_ = gm.getpolygon(lon,lat)

## split lake
test2 = gm.split_lake(poly,6e-04)
print(test2)

## get the coordinates of the centroids
markers = []
for idx,i in enumerate(test2):
        print((i.centroid.y, i.centroid.x))
        markers.append((i.centroid.y, i.centroid.x))




## GEt current coordinates of robot
# This coordinate will also be included in Genetic Algorithm #
# Add later #
# this will be the home coordinate


## Initiate the marker class
markersList = []
for i in range(len(markers)):
    markersList.append(GA.City(x=markers[i][0], y=markers[i][1]))

home = markersList[0]

## Marker mapping
mapping_dict = {}
for idx, i in enumerate(markersList):
    mapping_dict[i] = idx

print(mapping_dict)



bestpath = GA.geneticAlgorithm(population=markersList,home=home, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
print(type(bestpath))

for idx,i in enumerate(bestpath):
    # bestroute.append(mapping_dict[i])
    print(mapping_dict[i])