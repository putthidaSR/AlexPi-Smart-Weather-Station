# ***************************************************************************************************
# TCSS 573: Internet of Things (IoT)
# Winter 2021 | Final Project
#
# Group 10
# Name: Putthida Samrith, Jordan Overbo
# Date: March 14, 2021
# 
# File Name: AlexaSkill.py
#
# This script is written in Python3 to create a webserver instance using Flask, 
# detect values from GrovePi sensors, and communicate with Alexa Skill Kit Service on Cloud using Python package Flask-Ask 
# to build new skill sets for Alexa devices.
#
# This source code is inspired by the following resources:
# Flask-Ask: A New Python Framework for Rapid Alexa Skills Kit Development: 
# https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development
#
# Flask-Ask Official Documentation and Setup Guide: https://github.com/johnwheeler/flask-ask
# ***************************************************************************************************

import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
from grovepi import *

# Create the Flask instance. The Ask object is created by passing in the Flask application and a route to forward Alexa requests to.
# Source: https://flask-ask.readthedocs.io/en/latest/getting_started.html
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
 
# All values that are defined as synonyms in input commands
TEMP_COMMANDS = ['indoor temperature', 'temperature inside']
AIR_COMMANDS = ['air condition inside', 'air quality inside']

@ask.launch
def launch():
    welcomeSpeech = 'Welcome to the AlexPi - Your Personal Smart Meteorologist'
    return question(welcomeSpeech).reprompt(welcomeSpeech).simple_card('Hello!', welcomeSpeech)

# The intent decorator maps TemperatureIntent (defined in Amazon Alexa Skill Kit service) to a view function Indoor_Temperature_Intent.
@ask.intent('TemperatureIntent', mapping = {'Indoor_Temperature':'Indoor_Temperature'})
def Indoor_Temperature_Intent(Indoor_Temperature):
  
  # Read temperature and humidity values from Temperature Sensor
  temp_sensor = 3
  [temperature, humidity] = dht(temp_sensor, 0)
  
  print('**********************************Temperature')
  
  # Check if voice commands match the keywords to detect indoor temperature
  if Indoor_Temperature in TEMP_COMMANDS:
    
    # Alexa will play the statement and display the value on screen 
    # Displaying value on screen is only compatible with Alexa devices that have screen (ie: Echo Show)
    return statement('Temperature in your room is ' + str(int(temperature)) + 'celcius with the humidity of ' + str(humidity) + ' percent') \
        .standard_card(title='Indoor Temperature',
          text='Temperature: ' + str(temperature) + 'c\nHumidity: ' + str(humidity) + '%',
          small_image_url='https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/weather-icon-low.png',
          large_image_url='https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/weather-icon-high.png')
  
  # Command to play by Alexa device when Alexa could not understand your input command  
  else:
    return statement('Sorry, I could not understand your command. Please try again.')

# The intent decorator maps AirQualityIntent (defined in Amazon Alexa Skill Kit service) to a view function Indoor_Air_Intent.
@ask.intent('AirQualityIntent', mapping = {'Indoor_Air':'Indoor_Air'})
def Indoor_Air_Intent(Indoor_Air):
  
  # Read value from air quality sensor
  air_sensor = 0
  sensor_value = analogRead(air_sensor)
  
  # Check if voice commands match the keywords to detect indoor air quality
  if Indoor_Air in AIR_COMMANDS:
    
    # Map raw value from sensor to the specified air condition based on logic from https://wiki.seeedstudio.com/Grove-Air_Quality_Sensor_v1.3/
    
    # *******************************************************************************************************************
    # When detect low air pollution, prompt Alexa to ask user to turn on air purifier and wait for user's response 
    # while keeping the session open. Note that we only detect low air pollution here.
    # When we detect high pollution (raw value from sensor > 700), we use node-red to automatically turn on air purifier.
    # *******************************************************************************************************************
    if (sensor_value > 300):
      return question('We start to detect poor indoor air quality in your room. Should I turn on the air purifier?') \
          .reprompt('I did not get that. Would you like to turn on air purifier?').standard_card(title='Indoor Air Quality Condtion',
                         text='Indoor Air Quality: Low Pollution',
                         small_image_url='https://www.gstatic.com/webp/gallery3/1.png',
                         large_image_url='https://www.gstatic.com/webp/gallery3/2.png')
                         
    # *******************************************************************************************************************
    # When detect fresh air, Alexa will just play the statement and display the value on screen 
    # (compatible with Alexa devices that have screen only - ie: Echo Show)
    # *******************************************************************************************************************
    else:
      return statement('Air quality in your room is fresh air. We do not detect any pollution at the moment.') \
          .standard_card(title='Indoor Air Quality Condtion',
            text='Indoor Air Quality: Fresh Air',
            small_image_url='https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/air-quality-icon-low.png',
            large_image_url='https://tcss573-iot-thida.s3.us-east-2.amazonaws.com/air-quality-icon-high.png')
            
  # Command to play by Alexa device when Alexa could not understand your input command  
  else:
    return statement('Sorry, I could not understand your command. Please try again.')

# This help intent is pre-defined in Alexa Skill Kit service
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Start by Saying "Alexa, ask AlexPi..."'
    return question(speech_text).reprompt(speech_text).simple_card('AlexPi Help', speech_text)
 
@ask.session_ended
def session_ended():
    return "{}", 200

# Create a web server instance with the specified port number to setup a server using Flask
if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=5000)
