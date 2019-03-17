# Just a small homemade irrigation system
Just a small irrigation system for home plants
This file will be updated for each relevant update

## Arduino subsystem
Arduino subsystem tasks are:
- Fetch current temperature
- Fetch current humidity
- Fetch current moisture level

Currently following sensors are being used:
- DHT22 
- Capacitive moisture sensor. Check [Link](https://www.switchdoc.com/2018/11/tutorial-capacitive-moisture-sensor-grove/)
- RGB Led for human readable feedback from moisture sensor.

### Moisture level calibration
Following meausures have been taken:
- Dry situation: value measured &approx; 600
- Under water situation: value measured &approx; 360
- In soil. First measured &approx; 530. After 100 ml:
  - 14 min &approx; 510
  - 21 min &approx; 490
  - 35 min &approx; 475

## Daemon subsystem
Python daemon tasks are:
- Fetch temperature, humidity and moisture level from sensor and store it in a sqlite database
- Fecth temperature and humidity from OpenWeather and store it in a sqlite database

