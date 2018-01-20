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

#define echo2 9
#define trig2 10

int state = 0;

long distance1;
long distance2;
int duration1;
int duration2;

void setup() {
    //Sets up pins for ultrasonic tingz
    pinMode(echo1, INPUT);
    pinMode(trig1, OUTPUT);

    pinMode(echo2, INPUT);
    pinMode(trig2, OUTPUT);

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
    duration1 = pulseIn(echo1, HIGH);
    //Divide by speed of sound for distance in cm
    distance1 = duration1 / 58.0;

    //makes distance 0 if it is a dodgy number
    if (distance1 > 255 or distance1 < 0) {
        distance1 = 0;
        Serial.println("Distance not in transmission range");
    }
    else {
        Serial.println(distance1);
    }



    //Read proximity sensor data
    digitalWrite(trig2, HIGH);
    delayMicroseconds (50);
    digitalWrite(trig2, LOW);
    duration1 = pulseIn(echo2, HIGH);
    //Divide by speed of sound for distance in cm
    distance2 = duration2 / 58.0;

    //makes distance 0 if it is a dodgy number
    if (distance2 > 255 or distance2 < 0) {
        distance2 = 0;
        Serial.println("Distance not in transmission range");
    }
    else {
        Serial.println(distance2);
    }
}



void sendData(){

    //on 1st req, sends proximity sensor 1's distance
    if (state == 0) {
        Wire.write(distance1);
        state = state + 1;
    }
    //on 2nd req, sends a dummy number (for now)
    else if (state == 1){
        Wire.write(distance2);
        state = 0;
    }

}
