/*

Arduino code for home made irrigation system.
So far it uses:
- DHT22 for temperature and humidity. Pretty standard one.
- Capacitive Moisture Sensor. 
	Check https://www.switchdoc.com/2018/11/tutorial-capacitive-moisture-sensor-grove/

Author: Javi Robles (tjavier82)
	
*/

// Include Libraries
#include "DHT.h"


//Definitions
// Temperature and Humidity sensor
#define DHTTYPE DHT22

// Pin Definitions
// Digital
#define DHT_PIN_DATA	2

// Analog
#define MOISTURE_SENSOR 0


// Global values and objects
DHT dht(DHT_PIN_DATA, DHTTYPE);
const int TIMEOUT = 10000;      



// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    dht.begin();
}

void loop() 
{
  // DHT22/11 Humidity and Temperature Sensor
  // Reading humidity in %
  float dhtHumidity = dht.readHumidity();
  // Read temperature in Celsius, for Fahrenheit use .readTempF()
  float dhtTempC = dht.readTemperature();
	// Read moisture level
	int moistureLevel = analogRead(MOISTURE_SENSOR);

  Serial.print(dhtHumidity);Serial.print(";");Serial.print(dhtTempC);Serial.print(";");Serial.print(moistureLevel);Serial.println();
  delay(TIMEOUT);
    
}


