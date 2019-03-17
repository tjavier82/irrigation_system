/*

Arduino code for home made irrigation system.
So far it uses:
- DHT22 for temperature and humidity. Pretty standard one.
- Capacitive Moisture Sensor. 
	Check https://www.switchdoc.com/2018/11/tutorial-capacitive-moisture-sensor-grove/
- RGB Led to provide some human readable information
	
Author: Javi Robles (tjavier82)
	
*/

// Include Libraries
#include "DHT.h"


//Definitions
// Temperature and Humidity sensor
#define DHTTYPE DHT22

// Pin Definitions
// Digital
#define DHT_PIN_DATA 2
#define RED_PIN	3
#define GREEN_PIN 4
#define BLUE_PIN 5


// Analog
#define MOISTURE_SENSOR 0


// Global values and objects
DHT dht(DHT_PIN_DATA, DHTTYPE);
const int TIMEOUT = 10000;      

const int dry = 600;
const int wet = 360;
const int objectiveLevel = 480;
const int tolerance = 40;



// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    
	dht.begin();
	
	pinMode(RED_PIN, OUTPUT);
	pinMode(GREEN_PIN, OUTPUT);
	pinMode(BLUE_PIN, OUTPUT);
	
	// Off all leds
	digitalWrite(RED_PIN, LOW);
	digitalWrite(GREEN_PIN, LOW);
	digitalWrite(BLUE_PIN, LOW);
	
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

  
  // We set an objectiveLevel and check if we are in tolerance (good) or half tolerance (even better)
  if ((moistureLevel <= (objectiveLevel - tolerance))) {
	  //Too much water
	  //BLUE
	  color (0,0,255);
  }
  else if ((moistureLevel <= objectiveLevel - (tolerance/2))) {
	  //Some water excess
	  // CYAN
	  color (0, 255, 255);
  }
  else if ((moistureLevel >= objectiveLevel + (tolerance))) {
	  //Completely dry
	  //RED
	  color(255, 0, 0);
  }
  else if ((moistureLevel >= objectiveLevel + (tolerance/2))) {
	  //Some dryness
	  //ORANGE
	  color(237, 109, 0);
  }
  else {
	  //Everythong fine
	  //GREEN
	  color(0, 255, 255);
  }
  
  
  Serial.print(dhtHumidity);Serial.print(";");Serial.print(dhtTempC);Serial.print(";");Serial.print(moistureLevel);Serial.println();
  delay(TIMEOUT);
    
}

void color (int red, int green, int blue) {
	analogWrite(RED_PIN, red);
	analogWrite(GREEN_PIN, green);
	analogWrite(BLUE_PIN, blue);
}

