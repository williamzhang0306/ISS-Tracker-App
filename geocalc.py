import geopy
from geopy.geocoders import Nominatim
import math
from astropy import coordinates as coord
from astropy import units as u
from astropy import time
from astropy.time import Time
from datetime import datetime, timezone
import logging

ISO8601 =  "%Y-%jT%H:%M:%S.%fZ"

def get_lat_long(x:float, y:float, z:float, timestamp:str, time_format:str = ISO8601) -> tuple:
    """
    Computes latitude, longitude, and height from J2000 coordinates.

    Paramters:
    - x (float): x J2000 coordinate.
    - y (float): y J2000 coordinate.
    - z (float): z J2000 coordinate.
    - timestamp (string): UTC timestamp.
    - time_format (string): Format of the timestamp, default IS8601 standard.

    Returns:
    - tuple(lat, lon, height)
        - lat (float): latitude in decimal format.
        - long (float): longitude in decimal format.
        - height (str): string representation of height in km.

    Credit:
    https://stackoverflow.com/questions/78097446/how-do-i-use-astropy-to-transform-coordinates-from-j2000-to-lat-lon-and-altitu
    """
    dtime =  datetime.strptime(timestamp, time_format).replace(tzinfo=timezone.utc)
    now = Time(dtime)
    cartrep = coord.CartesianRepresentation(x,y,z, unit=u.km)

    gcrs = coord.GCRS(cartrep, obstime = now)
    itrs = gcrs.transform_to(coord.ITRS(obstime = now))
    loc = coord.EarthLocation(*itrs.cartesian.xyz)

    lat = float(loc.lat.to_string(decimal=True))
    lon = float(loc.lon.to_string(decimal=True))
    height = loc.height.to_string()

    logging.debug(f"Latitude {lat}, Longitude {lon}, height {height}")

    return lat, lon, height

def get_geoposition(lat:float ,long:float) -> str:
    """
    Searches for a geoposition associated with a coordinate.

     Paramters:
    - lat (float): latitude in decimal format.
    - long (float): longitude in decimal format.

    Returns:
    - string: the result of a geoposition query for the given coordinates.
    """
    geolocator = Nominatim(user_agent="UT-coe332-ISS-tracker-app")
    query = f"{lat}, {long}"
    location = geolocator.reverse(query, language='en')

    if location == None:
        return 'No location found.'
    elif type(location) == geopy.location.Location:
        return location.address
    else:
        return "Unexpected"

