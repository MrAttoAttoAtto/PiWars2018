/*
WIRING:
-------------------------------------------
  I2C
-------------------------------------------
  A4 = SDA -----> PI'S SDA = GPIO02 = PIN03
  A5 = SCL -----> PI'S SCL = GPIO03 = PIN05

  GND      -----> PI'S GND = PIN06
-------------------------------------------
  DISTANCE SENSOR 1
-------------------------------------------
  GND -----> GND
  VCC -----> +5V

  ECHO -----> D7
  TRIG -----> D8
 
 */

#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define echo1 7
#define trig1 8

int state = 0;

long distance;
int duration;

void setup() {
    //Sets up pins for ultrasonic tingz
    pinMode(echo1, INPUT);
    pinMode(trig1, OUTPUT);

    //Just for checking
    Serial.begin(9600);
    Serial.println("Ready!");

    //Initializes i2c and has a function run whenver a request comes in
    Wire.begin(SLAVE_ADDRESS);
    Wire.onRequest(sendData);
}

//Continously gets a distance reading, modifiying it if it is not ok
void loop() {

    //Read proximity sensor data
    digitalWrite(trig1, HIGH);
    delayMicroseconds (50);
    digitalWrite(trig1, LOW);
    duration = pulseIn(echo1, HIGH);
    //Divide by speed of sound for distance in cm
    distance = duration / 58.0;

    //makes distance 0 if it is a dodgy number
    if (distance > 255 or distance < 0) {
        distance = 0;
        Serial.println("Distance not in transmission range");
    }
    else {
        Serial.println(distance);
    }
}



void sendData(){

    //on 1st req, sends proximity sensor 1's distance
    if (state == 0) {
        Wire.write(distance);
        state = state + 1;
    }
    //on 2nd req, sends a dummy number (for now)
    else if (state == 1){
        Wire.write(1);
        state = 0;
    }

}
