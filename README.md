<h1 align="center">AlexPi - Smart Home Hub</h1>

<p align="center">
 <b><br>University of Washington Tacoma</b><br>
 <b>TCSS 573: Internet of Things – Winter 2021</b><br><br>
</p>

The purpose of this project is to design and implement a practical case of a smart home hub using Raspberry Pi. 

-----

## Project Structure Overview

```
├── Alexa
│   ├── AlexPi.json
│   ├── AlexaSkill.py
├── Grafana
│   ├── AlexPI_Advanced_Statistics_Dashboard.json
├── Node-Red
│   ├── AccountHandling-Flow.json
│   ├── AlexPi-Flow.json
│
```
- `Alexa/` : stored Python script to run Flask application and schema exported from Alexa Skill Kit service
- `Grafana/` : Stored Grafana JSON format dashboards
- `Node-Red/` : Stored Node-RED flows

-----

### Project Architecture
![ProjectArchitecture](https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/alexpi-architecture.png)

#### Our Technology Stacks:
- **Programming Language:** Python3, JavaScript
- **Database:** InfluxDB
- **Edge Dashboard:** Node-RED, Grafana
- **Other Services:** Amazon Alexa Skill Kit, ngrok, OpenWeatherMap API, AWS S3

#### Hardware Requirement:
- **Raspberry Pi 3 B+**
- **Grove - Temperature and Humidity Sensor:** Used for monitoring indoor temperature and humidity
- **Grove - Ultrasonic Sensor:** Used for detecting motion
- **Grove - Air Quality Sensor:** Used for monitoring indoor air quality conditions
- **Grove - Light Sensor:** Used for detecting indoor light
- **Grove - LED:** Used to indicate the status of indoor air quality, light detection and debugging
- **Amazon Echo Devices:** Echo Show (for voice command and display result on screen) and Echo Dot (for voice command)
- **Android or iOS device:** Used for receiving notifications and remotely sending voice commands (through Alexa mobile app)
- **Alexa-Compatible Smart Devices (Smart bulb and smart plug):** Used for controlling and automating smart home

-----

### Overview of Required Steps to Run the Project:
1. Expose a local web server to the Internet:
    - Create ngrok account
    - Configure ngork on Raspberry Pi
2. Configure new Alexa Skill on Amazon Alexa Skill Kit Service:
    - Create Amazon Developer account
    - Create new Alexa Skill on Amazon Alexa Skill Kit Service
3. Install Flask and Flask_Ask to write Python3 script and run Flask application locally
4. Configure InfluxDB on Raspberry Pi
5. Connect required sensors to GrovePi board
6. Install node-red-contrib-alexa-remote2 package on Node-RED and configure it with Amazon Alexa account
7. Integrate Grafana with InfluxDB

**In this project, we will be running two web servers concurrently with different port numbers:**
- 5000: Run Flask application to build new Alexa skills with Amazon Alexa Skill Kit Service on Cloud
- 8086: Run Node-Red to launch local IoT dashboard, control smart devices and insert data into InfluxDB

-----

## The rest of the documentation provide more detail on how to setup the required steps above.

### Expose a local web server to the internet:

We use ngrok to expose a web server running on our Raspberry Pi to be publicly accessbile on the Internet so that it can communicate with Alexa Skill Kit Service.

- Create a free ngrok account: dashboard.ngrok.com/signup
- Copy the authentication token found in your ngrok dashboard
- Open Terminal and run the following commands to download and install ngrok:
        `wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip`
        `unzip ngrok-stable-linux-arm.zip`
- Connect to your account with the authentication token copied from your ngrok account:
        `./ngrok authtoken <AUTH_TOKEN>`
- Start a HTTP tunnel forwarding to your local port 5000:
        `./ngrok http 5000`
- Copy the Forwarding HTTPS URL on the terminal (You will need this endpoint when you configure Alexa Skill Kit Service later)
- Do not close the ngrok terminal. Keep it running.

Full instruction on how to setup ngrok on Raspberry Pi can be found here: `https://www.dexterindustries.com/howto/access-your-raspberry-pi-from-outside-your-home-or-local-network/`

### How to configure new Alexa Skill on Amazon Alexa Skill Kit Service

- Create Amazon Developer Account: `https://developer.amazon.com/`
- Open Developer Console and launch Alexa Skill Kit: `https://developer.amazon.com/alexa/console/ask`
- Create a new skill and fill in the required fields based on your developer environment
- Launch the newly created skill
    - Expand Interaction Model and go to JSON Editor: Paste in the JSON file (AlexPi.json) from the /alexa directory
    - Go to Endpoint menu and select HTTPS: In Default Region section, paste in the HTTPS URL generated from ngrok
- Save and click on Build Model

### How to Run the Flask Application:
- Once you get the above steps setup, open terminal and navigate to where you store AlexaSkill.py file, - Run: `python3 AlexaSkill.py` (or run directly from IDE)

### Configure InfluxDB on Raspberry Pi
- Install InfluxDB on the Local Raspberry Pi
- Create User with with all priviledges
- Create Database on the InfluxDB server that has been created locally
- Install `node-red-contrib-influxdb` package on Node-RED
- Configure the InfluxDB output and input nodes on both node red flows using the user and database that was created.

### Configure Node-RED
- Install `node-red-contrib-alexa-remote2` package on Node-RED and configure it with your Amazon Alexa account
- Navigate to `Node-Red` directory in this project source code and import `AccountHandling-Flow.json` and `AlexPi-Flow.json` to Node-RED
- Update any Alexa Routine Nodes in Smart Weather flow to match with your smart home devices
- Update any sensors in Smart Weather flow to match with your Raspberry Pi and GrovePi setup
- Update any influxdb-out node on both AccountHandlig and Smart Weather flows

### Integrate Grafana with InfluxDB
- Install Grafana and run on the Local Raspberry Pi
- Create User Account on Grafana.
- Add Datasource on grafana, configure it to the created InfluxDB database
- Select new Dashboard and import `AlexPi_Advanced_Statistics_Dashboard.json` from the /Grafana directory
- Configure time series and username to your liking

----

## Developer Notes
- We are using the free version of ngrok so we do not have any reserved domains for the endpoint. For free version, the HTTPS URL endpoint from ngrok is updated each time you start a tunnel. You must also update Endpoint on Alexa Skill Kit service with the new HTTPS endpoint each time the endpoint from ngrok is changing.
- The Flask web server is running on port 5000. If you already use this port number for other purposes, please update the port number in AlexaSkill.py file.


## Application Screenshots
| AlexPi Setup |
| :------: |
|<img src="https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/alexpi-hardware.png" width="500">|

| Edge-based IoT Dashboard (Node-RED) | Edge-based IoT Dashboard (Grafana) |
| :------: | :--------: |
| ![Node-red](https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/IoT+edge+dashboard.jpg) | ![Grafana](https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/grafana-dashboard.png) |
