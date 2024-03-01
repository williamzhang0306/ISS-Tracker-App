import pytest
from iss_tracker import *

# NOTE: Unit tests for Flask routes were generated with the aid of ChatGPT

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_load_from_NASA():
    '''
    A test case to check if xml data can still be retrieved
    and parsed from NASA
    '''
    data = load_iss_data_from_url(iss_data_url)

def test_search_epochs():
    '''
    Tests 'normal' usage of search_epochs, usage on an empty data set,
    and usage with an invalid timestamp
    '''
    # normal 
    data = load_iss_data_from_url(iss_data_url)    
    search_epochs( provided_epoch_str="NOW", list_state_vectors= data)

    # empty data set
    assert( search_epochs( provided_epoch_str="NOW", list_state_vectors=[]) == {})

    # invalid key
    with pytest.raises(ValueError):
        search_epochs( provided_epoch_str="Not_Valid", list_state_vectors=[])

def test_speed_at_epoch():
    normal_data = {
        "X_DOT": {
        "#text": "2",
        "@units": "km/s"
        },
        "Z_DOT": {
        "#text": "3",
        "@units": "km"
        },
        "Y_DOT": {
        "#text": "6",
        "@units": "km/s"
        }
    }

    assert ( speed_at_epoch(normal_data) - 7 < 0.0001)


    bad_data = {
        "": {
        "#text": "3",
        "@units": "km"
        },
        "Y_DOT": {
        "#text": "6",
        "@units": "km/s"
        }
    }

    with pytest.raises(KeyError):
        speed_at_epoch(bad_data)
    
def test_get_epochs(client):
    response = client.get('/epochs?limit=5&offset=0')
    assert response.status_code == 200
    # Add more assertions based on the expected behavior of your route

def test_get_single_epoch(client):
    response = client.get('/epochs/2022-01-01T00:00:00.000Z')
    assert response.status_code == 200
    # Add more assertions based on the expected behavior of your route

def test_get_single_epoch_speed(client):
    response = client.get('/epochs/2022-01-01T00:00:00.000Z/speed')
    assert response.status_code == 200
    # Add more assertions based on the expected behavior of your route

def test_get_current_epoch(client):
    response = client.get('/now')
    assert response.status_code == 200
    # Add more assertions based on the expected behavior of your route