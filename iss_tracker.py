#!/usr/bin/python3
import requests
from flask import Flask, request
import xmltodict
import logging
from typing import List
from datetime import datetime, timezone, timedelta
import math

# Current URL to access ISS data
iss_data_url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'

# initialize flask app
app = Flask(__name__)

def load_iss_data_from_url(url: str, return_type = 'epochs') -> List[dict]:
    '''
    Loads state vector data of the ISS from a given URL.

    Arguments:
    - url (str): The URL to fetch ISS data from.
    - return_type (str): ['header','metadata','epochs','comments']

    Returns:
    - List[dict]: A list of state vector data for the ISS.
    '''
    # GET data from web
    response = requests.get(url)

    # Check if the GET request failed
    response.raise_for_status()

    # Load XML data into python dict.
    try:
        xml_binary = response.content
        data = xmltodict.parse(xml_binary)
    except:
        logging.warning(f'Failed load XML data to dict.')
        return []

    # Parse and return specificed data from dict
    if return_type == 'header':
        try:
            header = data['ndm']['oem']['header']
        except:
            logging.warning(f'Failed load XML data to dict.')
            header = []
        return header
    

    elif return_type == 'metadata':
        try:
            metadata =  data['ndm']['oem']['body']['segment']['metadata']
        except:
            logging.warning(f'Failed load XML data to dict.')
            metadata = []
        return metadata
    

    elif return_type == 'epochs':
        try:
            epochs = data['ndm']['oem']['body']['segment']['data']['stateVector']
        except:
            logging.warning(f'Failed load XML data to dict.')
            epochs = []
        return epochs
    

    elif return_type == 'comments':
        try:
            comments = data['ndm']['oem']['body']['segment']['data']['COMMENT']
        except:
            logging.warning(f'Failed load XML data to dict.')
            comments = []
        return comments
    
    else:
        raise ValueError(f"Invalid return type {return_type}. Choose ['header','metadata','epochs','comments'].")

def search_epochs(
    provided_epoch_str:str,
    list_state_vectors: List[dict],
    epoch_key:str = 'EPOCH', 
    provided_epoch_format:str = "%Y-%jT%H:%M:%S.%fZ",
    data_epoch_format:str = "%Y-%jT%H:%M:%S.%fZ"
) -> dict:
    """
    Finds the state vector with the nearest epoch timestamp in the given list.

    Parameters:
    - provided_epoch_str (str): The time stamp of the specific epoch to search for.
    - list_state_vectors (List[dict]): A list of dictionaries containing state vectors.
    - epoch_key (str, optional): The key in each dictionary representing the epoch timestamp.
      Defaults to 'EPOCH'.
    - provided_epoch_format (str, optional): The format of the timestamp to search for.
      Defaults to "%Y-%jT%H:%M:%S.%fZ".
    - data_epoch_format (str, optional): The format of the time stamps in the data
      Defaults to "%Y-%jT%H:%M:%S.%fZ".

    Returns:
    - dict: The state vector dictionary with the nearest epoch timestamp.
    """
    
    # default is use time stamp for when function was executed:
    try:
        if provided_epoch_str == "NOW":
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
        else:
            now = datetime.strptime(provided_epoch_str, provided_epoch_format).replace(tzinfo=timezone.utc)
    except:
        raise ValueError(f"Provided Time Stamp unrecognized: {provided_epoch_str}.")

    # Search for the nearest epoch by timestamp
    closest_epoch = {}
    smallest_distance = timedelta.max
    for item in list_state_vectors:

        # get item's timestamp
        try:
            timestamp = item[epoch_key]
        except KeyError:
            logging.warning(f'Data missing key: {epoch_key}')
            continue
        
        # calculate temporal distance from "now" to item's timestamp 
        item_datetime = datetime.strptime(timestamp, data_epoch_format).replace(tzinfo=timezone.utc)
        distance = abs(now - item_datetime)
        if distance < smallest_distance:
            # update when a closer item is found
            closest_epoch = item
            smallest_distance = distance

    return closest_epoch

def speed_at_epoch(data_point:dict):
    """
    Calculates the speed magnitude from the velocity components in the given data point.

    Parameters:
    - data_point (dict): A dictionary containing velocity components.

    Returns:
    - float: The magnitude of the velocity vector.
    """

    x_dot = float(data_point['X_DOT']['#text'])
    y_dot = float(data_point['Y_DOT']['#text'])
    z_dot = float(data_point['Z_DOT']['#text'])

    return math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)

### Flask Routes:
@app.route('/epochs', methods = ['GET'])
def get_epochs():
    '''
    Flask route that retrieves epochs data. Additionally accepts
    query paramters limit and offset.

    Usage:
    `curl <host>:<port>/epochs?limit=int&offset=int`

    Parameters:
    - limit (int, optional): The maximum number of epochs to return
    - offset (int, optional): Offset of 
    '''

    # get query paramters
    limit = request.args.get('limit', '1000000')
    if not limit.isnumeric():
        logging.debug('Recieved nonnumeric user input:', limit)
        return "Error: Query parmeter 'limit' must be an integer."
    limit = int(limit)

    offset = request.args.get('offset', '0')
    if not offset.isnumeric():
        logging.debug('Recieved nonnumeric user input:', offset)
        return "Error: Query parmeter 'offset' must be an integer."
    offset = int(offset)

    # retrieve data from NASA
    try:
        data = load_iss_data_from_url(iss_data_url)
    except requests.HTTPError as e:
        return f'Failed to retreieve ISS data from NASA. Status Code: {e.response.status_code}'

    # get the queried part of the data
    if limit == -1 or offset+limit > len(data):
        return data[offset:-1]

    else:
        return data[offset:offset+limit]

@app.route('/epochs/<epoch>', methods = ['GET'])
def get_single_epoch(epoch):
    # retrieve data from NASA
    try:
        data = load_iss_data_from_url(iss_data_url)
    except requests.HTTPError as e:
        return f'Failed to retreieve ISS data from NASA. Status Code: {e.response.status_code}'
    
    # get the closest epoch
    try:
        closest_epoch = search_epochs(epoch, data)
        return closest_epoch
    except:
        return f'Failed to find {epoch} in data range.'

@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def get_single_epoch_speed(epoch):
    # retrieve data from NASA
    try:
        data = load_iss_data_from_url(iss_data_url)
    except requests.HTTPError as e:
        return f'Failed to retreieve ISS data from NASA. Status Code: {e.response.status_code}'
    
    # get the closest epoch
    try:
        closest_epoch = search_epochs(epoch, data)
    except:
        return f'Failed to find {epoch} in data range.'
    
    # Get speed at closest epoch
    return str(speed_at_epoch(closest_epoch))

@app.route('/epochs/<epoch>/location', methods = ['GET'])
def get_single_epoch_location(epoch):
    # retrieve data from NASA
    try:
        data = load_iss_data_from_url(iss_data_url)
    except requests.HTTPError as e:
        return f'Failed to retreieve ISS data from NASA. Status Code: {e.response.status_code}'
    
    # get the closest epoch
    try:
        closest_epoch = search_epochs(epoch, data)
    except:
        return f'Failed to find {epoch} in data range.'
    
    # Get speed at closest epoch
    return str(speed_at_epoch(closest_epoch))


@app.route('/now', methods = ['GET'])
def get_current_epoch():
    # retrieve data from NASA
    try:
        data = load_iss_data_from_url(iss_data_url)
    except requests.HTTPError as e:
        return f'Failed to retreieve ISS data from NASA. Status Code: {e.response.status_code}'
    
    # get the closest epoch
    try:
        closest_epoch = search_epochs('NOW', data)
    except:
        return f"Failed to find 'NOW' in data range."
    
    # Repackage epoch data
    position_vector = [float( closest_epoch[position_key]["#text"]) for position_key in ["X", "Y", "Z"]]
    velocity_vector =  [float( closest_epoch[velocity_key]["#text"]) for velocity_key in ["X_DOT", "Y_DOT", "Z_DOT"]]
    speed = speed_at_epoch(closest_epoch)

    packet = {
        "position": position_vector,
        "velocity": velocity_vector,
        "speed": speed
    }

    return packet


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
