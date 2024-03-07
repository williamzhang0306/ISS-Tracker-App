# ISS-Tracker-App
This repository contains the code and instructions to build, run and test a containerized flask service that provides up to date  information on the International Space Station's (ISS) trajectory. The provides flask routes for retreiving and filter the data from NASA's public data repository [[1]](#citations). 

# Table of Contents

1. [Software Diagram](#software-diagram)
2. [Directory Summary](#content)
3. [Usage](#usage)
4. [Citations](#citations)

# Software Diagram


The Jestream VM can be accessed via a two hop SSH connection. First into the student-login node at TACC, then into a virtual machine. Within the VM, a client can send requests to the containerized ISS Tracker app. The python script running within the container uses the Flask API to manage the requests. Additionally the python script uses the requests library to pull the NASA data set and performs processing/filtering before sending the data to the client.

# Directory Summary

```
ISS-TRACKER-APP/
├── docker-compose.yml
├── dockerfile
├── geocalc.py
├── iss_tracker.py
├── test_iss_tracker.py
├── README.md
└── requirements.txt
```
1. `dockerfile` - The instructions used by docker to create the iss_tracker docker image.
2. `docker-compose.yml` - A configuration file to help manage and run containers
3. `geocalc.py` - A library
4. `iss_tracker.py` - The python script that retrieves ISS state vector data and provides Flask routes to access the data.
5. `test_iss_tracker.py` - Pytest compatible unit tests for the all the functions in iss_tracker.py.
6. `requirements.txt` - A list of python dependencies for this app.


# Usage
Prerequiste: An enviornment with Docker installed. 

## With Docker Commands

### Docker Build

To build the iss_tracker Docker image run the `docker build` command from the `homework04` directory:

```bash
docker build -t williamzhang/flask-iss-tracker:1.0 .
```
This will build a Docker image tagged `williamzhang/flask-iss-tracker:1.0` using the Dockerfile in the this directory.

### Docker Run

After building the image, you can run the `iss_tracker.py` script as a docker container,
```bash 
docker run --name "flask-iss-app" -d -p 5000:5000 williamzhang/flask-iss-tracker:1.0
```
Here's a summary of the options for `docker run`:
+ `--name "flask-iss-app"`: Sets a custom name ("flask-iss-app") for the container.

+ `-d`: Runs the container in the background (detached mode).

+ `-p 5000:5000`: Publishes the container's port 5000 to the host machine's port 5000.

+ `williamzhang/flask-iss-tracker:1.0`: Specifies the Docker image to use for creating the container. In this case, it uses the image named "williamzhang/flask-iss-tracker" with the tag "1.0".

## With Docker Compose
Alternatively, you can use the docker compose file which has already configured the service.

To build the flask-iss-tracker image run:
```bash 
docker compose build
```

Then to launch the service in the background run.
```bash
docker compose up -d
```

## Accessing Routes

While the service is running it provides multiple Flask routes for accessing ISS trajectory data.

- [`/comment`](#`/comment`)
- [`/header`](#`/headert`)
- [`/metadata`](#`/metadata`)
- [`/epochs?limit=int&offset=int`](#/epochs?limit=int&offset=int)
- [`/epochs/<epoch>`](#/epochs/<epoch>)
- [`/epochs/<epoch>/speed`](#`/epochs/<epoch>/speed`)
- [`/epochs/<epoch>/location`](#/epochs/<epoch>/location``)
- [`/now`](#`/now`)

### `/comment`:

This route will retrieve the 'comment' list data.

Example:
```shell
curl "localhost:5000/comment"
```
Output:
```shell
[
  "Units are in kg and m^2",
  "MASS=459325.00",
  "DRAG_AREA=1487.80",
  "DRAG_COEFF=1.85",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2024-03-04T12:26:27.616 $ ORBIT = 231 $ LAN(DEG) = 124.75313",
  "ISS last asc. node : EPOCH = 2024-03-19T11:33:05.982 $ ORBIT = 463 $ LAN(DEG) = 49.27177",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "Crew-8 Docking        065:08:00:00.000             0.0     422.5     412.8",
  "(0.0)   (228.1)   (222.9)",
  null,
  "Crew-7 Undock         071:15:00:00.000             0.0     423.8     410.2",
  "(0.0)   (228.9)   (221.5)",
  null,
  "GMT073 Reboost Preli  073:13:59:00.000             1.5     424.2     409.5",
  "(4.9)   (229.1)   (221.1)",
  null,
  "SpX-30 Launch         075:23:13:00.000             0.0     424.5     413.8",
  "(0.0)   (229.2)   (223.4)",
  null,
  "SpX-30 Docking        077:11:00:00.000             0.0     424.9     413.4",
  "(0.0)   (229.4)   (223.2)",
  null,
  "=============================================================================",
  "End sequence of events"
]
```

### `/header`

This route will retrieve the ISS trajectory dataset header.

Example:
```shell
curl "localhost:5000/header"
```
Output:
```shell
{
  "CREATION_DATE": "2024-064T19:05:34.727Z",
  "ORIGINATOR": "JSC"
}
```


### `/metadata`

This route will retrieve the ISS trajectory dataset metadata.

Example:
```shell
curl "localhost:5000/header"
```
Output:
```shell
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2024-064T12:00:00.000Z",
  "STOP_TIME": "2024-079T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
```

### `/epochs?limit=int&offset=int`
This route will provide the avaible epochs data within the optional query paramters:
- `limit`: the maxmium number of epochs to return
- `offset`: the number of epochs to skip from the start of avaible data.

Without passing any paramters, this route wiil return the entirety of the avaible data.

Example:
```shell
curl localhost:5000/epochs
```
Output:
```shell
[
 {
    "EPOCH": "2024-067T11:54:00.000Z",
    "X": {
      "#text": "-4163.3534725972404",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-1.1474439071968301",
      "@units": "km/s"
    },
    "Y": {
      "#text": "2583.6625281637798",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-7.0238470668305402",
      "@units": "km/s"
    },
    "Z": {
      "#text": "4699.48974739803",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "2.8444416176628402",
      "@units": "km/s"
    }
  },
  
  ...

  {
    "EPOCH": "2024-067T11:58:00.000Z",
    "X": {
      "#text": "-4283.9472609613204",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "0.14844509525019001",
      "@units": "km/s"
    },
    "Y": {
      "#text": "824.44392134937004",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-7.5467160106393596",
      "@units": "km/s"
    },
    "Z": {
      "#text": "5202.40213205689",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "1.3210479505166799",
      "@units": "km/s"
    }
  }
]
```

With `limit` = 1 and `offset` = 10. This should return just the 10th availble epoch and nothing more.

Example:
```shell
curl localhost:5000/epochs?limit=1&offset=10
```
Output:
```shell
[
  {
    "EPOCH": "2024-052T12:00:00.000Z",
    "X": {
      "#text": "4721.5105798739096",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-5.4614207249789404",
      "@units": "km/s"
    },
    "Y": {
      "#text": "2692.6387190393002",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "3.72333576790653",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-4082.3502740408699",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-3.8618306484028202",
      "@units": "km/s"
    }
  }
]
```


### `/epochs/<epoch>`

You can serach for the data associated with an individual epoch. Note that the app expects the epoch to be provided in ISO8601 format. In other words provide a UTC time stamp in this format `{Year}-{Day of the year}T{HH:MM:SS.MS}Z`. For example "2024-052T11:35:00.01Z".

Example:
```shell
curl localhost:5000/epochs/2024-63T11:35:00.01Z
```
Output:
```shell
{
  "EPOCH": "2024-064T12:00:00.000Z",
  "X": {
    "#text": "4353.7916429999996",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-2.0891359660000002",
    "@units": "km/s"
  },
  "Y": {
    "#text": "318.43206900000001",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "7.2463633099999996",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-5212.534463",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-1.2973529509999999",
    "@units": "km/s"
  }
}
```

### `/epochs/<epoch>/speed`

If you are just interested in the speed at a certain epoch, adding `/speed` will return the magnitude of the velocity vector in km/s.

Example:
```shell
curl localhost:5000/epochs/2024-63T11:35:00.01Z/speed
```
Output:
```shell
7.65228037805838
```

### `/epochs/<epoch>/location`

Similarly, adding `/location` instead will return the latitude, longitude, altitude and geolocation at the epoch.

Example:
```shell
curl localhost:5000/epochs/2024-67T14:50:00.01Z/location
```
Output:
```shell
{
  "Altitude": "415.8499382971738 km",
  "Geolocation": "Kishoreganj, Kishoreganj Sadar, Kishoreganj District, Dhaka Division, Bangladesh",
  "Latitude": 24.357,
  "Longitude": 90.8335
}

```

### `/now`

This route will search for the epoch closest to when the request is sent and return the Altitude, Geolocation, Latitude, Longitude, ISO time stamp, speed, position and velocity.

Example:
```shell
curl localhost:5000/now
```
Output:
```shell
{
  "Altitude": "424.2398040187759 km",
  "Geolocation": "No location found.",
  "Latitude": 38.2895,
  "Longitude": -131.181,
  "epoch": "2024-067T13:44:00.000Z",
  "position": [
    -2640.37989455653,
    -4642.18843325062,
    4199.96698288328
  ],
  "speed": 7.6597976929977465,
  "velocity": [
    3.79549286476059,
    -5.52509302275157,
    -3.70676161914237
  ]
}
```


## Citations
1. Keeter, B. (Page Editor), & Keaton, J. (NASA Official). (2022, July 11). ISS Trajectory Data. Spot The Station. National Aeronautics and Space Administration. https://spotthestation.nasa.gov/trajectory_data.cfm