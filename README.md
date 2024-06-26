# SensoriX
SensoriX is a cloud computing and data analysis project made by a team of HTL students. The project can be deployed with a Docker compose file and is made to work within the school facility. The goal is to fetch data from sensors, load them into a mongoDb and display them in the browser using the Python Flask library.


## Features
- Realtime data fetching
- Physical measurements of wifi-traffic, power generation using solar membrans, and the temperature in one of the school rooms
- Graph display and table view of the proccessed data in the webserver
- Deployability using Docker container technology
- consistent saving of measurement entries using docker volumes for the mongoDB


# How to deploy
The following guide will walk you through how you too can deploy this project!

## Prerequisites
- Docker (either locally installed or on one of the schools virtual machines)

## Step 1
pull or download the root of our project:
```git pull https://github.com/Imperator07/SensoriX.git```

if you want to use a virtual machine you also have to transfer the folder onto it.

## Step 2
Using some shell navigate to the root/pycharm - project directory and run:
```docker compose -f .\docker_compose.yaml up -d --build```

## Step 3
to view the browser site you must go into the url field of your prefered browser and enter the IP-Adress of your laptop or virtual machine followed by ":5000". This will specify the port the python webserver operates on.
