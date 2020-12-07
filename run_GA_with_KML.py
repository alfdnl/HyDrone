import HyD
from sensors import Sensor as s
import os
from pykml import parser
import generate_map as gm
import folium
import time
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import genetic_algorithm_TSP as GA
from folium.features import DivIcon

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
m = gm.printMap([3.1189078118594447,101.65878139637647],100,poly)
for idx,i in enumerate(test2):
    folium.GeoJson(i).add_to(m)
    folium.Marker([i.centroid.y, i.centroid.x]).add_to(m)
    folium.Marker([i.centroid.y,i.centroid.x], icon=DivIcon(
        icon_size=(10,10),
        icon_anchor=(4,63),
        html='<div style="font-size: 14pt; color : red">{}</div>'.format(idx),
        )).add_to(m)
m



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

m = folium.Map([3.1189078118594447,101.65878139637647], zoom_start=100, tiles='cartodbpositron')
## Add marker
for idx,i in enumerate(bestpath):
    print(mapping_dict[i])
    folium.Marker([i.x,i.y]).add_to(m)
    folium.Marker([i.x,i.y], icon=DivIcon(
        icon_size=(10,10),
        icon_anchor=(4,63),
        html='<div style="font-size: 14pt; color : red">{}</div>'.format(idx),
        )).add_to(m)
m
    # m.save('templates/map.html')

