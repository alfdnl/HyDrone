from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
import folium

proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')


def geodesic_point_buffer_marker(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(3)  # distance in metres
    return transform(project, buf)

def geodesic_point_buffer_robot(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(1)  # distance in metres
    return transform(project, buf)

# Example
b = geodesic_point_buffer_marker(3.119629449776096, 101.65642710502878, 0.01)
type(b)
point = geodesic_point_buffer_robot(3.119570613676185, 101.65657144167113, 0.01)
m = folium.Map([3.1189078118594447, 101.65878139637647], zoom_start=12, tiles='cartodbpositron')
folium.GeoJson(b).add_to(m)
folium.GeoJson(point).add_to(m)
folium.LatLngPopup().add_to(m)

m
print(type(b))
point.intersects(b)