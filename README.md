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
```bash 
[1] docker compose build
[2] docker compose up -d
```

## Accessing Routes

The app has multiple different routes for accessing ISS trajectory data.

### `/comment`:

This route will retrieve the 'comment' list data.

Example:
```shell
$ curl "localhost:5000/comment"
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
### `/metadata`
### `/epochs?limit=int&offset=int`
### `/epochs/<epoch>`
### `/epochs/<epoch>/speed`
### `/epochs/<epoch>/location`
### `/now`


## Citations
1. Keeter, B. (Page Editor), & Keaton, J. (NASA Official). (2022, July 11). ISS Trajectory Data. Spot The Station. National Aeronautics and Space Administration. https://spotthestation.nasa.gov/trajectory_data.cfm