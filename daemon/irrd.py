
# Reads information from Arduino and stores it into a sqllite db

import logging
import serial
import time
import configparser
import argparse
import pyowm
import sqlite3

DEFAULT_CONFIG_FILE = "config.ini"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file. If not provided, " + DEFAULT_CONFIG_FILE + " will be used.",
                        default=DEFAULT_CONFIG_FILE)
    parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")
    args = parser.parse_args()


    config = configparser.ConfigParser()
    try:
        config.read (args.config)
    except:
        print ('Error reading config file')
        exit()

    #Setting up logs
    logger =  logging.getLogger(config['Logging']['LoggerName'])
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    #Setting up config options. Config file will have following sections
    # Serial
    #   SerialPort
    #   SerialBaudRate
    #   SerialTimeout
    #   SleepTime
    #
    # Database
    #   FilePath
    #
    # Logging
    #   LoggerName
    #
    # OpenWeather
    #   APIKey
    #   Lat
    #   Lon


    serial_port = config['Serial']['SerialPort']
    serial_baud_rate = int(config['Serial']['SerialBaudRate'])
    serial_timeout = int(config['Serial']['SerialTimeout'])
    sleep_time = int(config['Serial']['SleepTime'])
    db_file = config['Database']['FilePath']
    lat = float(config['OpenWeather']['Lat'])
    lon = float(config['OpenWeather']['Lon'])

    owm = pyowm.OWM(config['OpenWeather']['APIKey'], language='es')
    go_on = True

    while go_on:
        try:

            # Getting weather object.
            obs = owm.weather_at_coords(lat, lon)
            w = obs.get_weather()

            # Opening connection to database and arduino.
            db = sqlite3.connect(db_file)
            cursor = db.cursor()
            arduino = serial.Serial(serial_port, serial_baud_rate, timeout=serial_timeout)


            # Get information and insert tinto database
            hour = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            temp_at_coords = w.get_temperature('celsius')['temp']
            logger.debug('Value read: ' + str(temp_at_coords) + ' at ' + hour)

            cursor.execute('''INSERT INTO temperatureRead(temperature, type, date)
                              VALUES (?,?,?)''', (temp_at_coords, 'outside', hour))

            humidity_at_coords = w.get_humidity()
            logger.debug('Value read: ' + str(humidity_at_coords) + ' at ' + hour)

            cursor.execute('''INSERT INTO humidityRead(humidity, type, date)
                              VALUES (?,?,?)''', (humidity_at_coords, 'outside', hour))

            a = arduino.readline().strip().decode('ascii')
            logger.debug('Value read: ' + str(a) + ' at ' + hour)

            humidity = float(a.split(';')[0])
            temperature = float(a.split(';')[1])
            moisture = int(a.split(';')[2])

            cursor.execute('''INSERT INTO humidityRead(humidity, type, date)
                              VALUES (?,?,?)''', (humidity, 'inside', hour))
            cursor.execute('''INSERT INTO temperatureRead(temperature, type, date)
                              VALUES (?,?,?)''', (temperature, 'inside', hour))
            cursor.execute('''INSERT INTO moistureRead(moisture, plant, date)
                              VALUES (?,?,?)''', (moisture, 'smiley', hour))

            # Closing everything. Sleep time will be around 10 minutes so it does not make sense keeping it open
            db.commit()
            cursor.close()
            db.close()
            arduino.close()

            # Sleeeeeeeeeep
            time.sleep(sleep_time)

        except pyowm.exceptions.api_call_error.APICallTimeoutError:
            logger.exception('OWM API Timeout')

        except:
            logger.exception('Exception not cached, exiting...')
            cursor.close()
            db.close()
            arduino.close()
            go_on = False


