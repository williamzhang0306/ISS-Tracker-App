import geopy
from geopy.geocoders import Nominatim
import math

def geo_calculate(x,y,z):
    '''
    Given cartesian coordinates X Y Z, calculate longitude, latitude and altitude.

    Paramters
    - x , y , z (float): coordinates in 3d space relative to the centroid of Earth.
                         Units in km
    
    Returns:
    - lat (float): lattitude in degrees
    - long (float): longitude in degrees
    - alt (float): altitude above surface in km

    Credit:
    - Copied heavily from this stackoverflow answer.
    https://stackoverflow.com/questions/56945401/converting-xyz-coordinates-to-longitutde-latitude-in-python
    '''
    a = 6378.137 #in meters
    b = 6356.752314245 #in meters

    f = (a - b) / a
    f_inv = 1.0 / f

    e_sq = f * (2 - f)                       
    eps = e_sq / (1.0 - e_sq)

    p = math.sqrt(x * x + y * y)
    q = math.atan2((z * a), (p * b))

    sin_q = math.sin(q)
    cos_q = math.cos(q)

    sin_q_3 = sin_q * sin_q * sin_q
    cos_q_3 = cos_q * cos_q * cos_q

    phi = math.atan2((z + eps * b * sin_q_3), (p - e_sq * a * cos_q_3))
    lam = math.atan2(y, x)

    v = a / math.sqrt(1.0 - e_sq * math.sin(phi) * math.sin(phi))
    h   = (p / math.cos(phi)) - v

    lat = math.degrees(phi)
    lon = math.degrees(lam)

    return lat, lon, h

def get_geoposition(lat,long):
    geolocator = Nominatim(user_agent="UT-coe332-ISS-tracker-app")
    query = f"{lat}, {long}"
    location = geolocator.reverse(query, language='en')

    if location == None:
        return 'No location found.'
    elif type(location) == geopy.location.Location:
        return location.address
    else:
        return "Unexpected"

