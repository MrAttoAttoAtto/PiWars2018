#include <Wire.h>

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


#define SLAVE_ADDRESS 0x04


volatile int state = 0;

byte echoPins[] = {7, 9, 11};
byte triggerPins[] = {8, 10, 12};
long durations[] = {0,0,0};
volatile int distances[] = {0,0,0};

uint16_t i;
uint16_t j = 0;



void setup() {
    // Sets up echo inputs, and trigger outputs
    for (i=0;i<3;i++){
      pinMode(echoPins[i], INPUT);
      pinMode(triggerPins[i], OUTPUT);
    }

    

    //Just for checking
    Serial.begin(9600);
    Serial.println("Ready!");



    //Initializes i2c and has a function run whenver a request comes in
    Wire.begin(SLAVE_ADDRESS);
    Wire.onRequest(sendData);
}

//Continously gets a distance reading, modifiying it if it is not ok
void loop() {
    Serial.println("---");
    for (i=0; i<3; i++) {
      digitalWrite(triggerPins[i], HIGH);
      delayMicroseconds(50);
      digitalWrite(triggerPins[i], LOW);
      durations[i] = pulseIn(echoPins[i], HIGH, 8000);
      distances[i] = durations[i] / 58.3;
      //makes distance 0 if it is a dodgy number
      if (distances[i] > 255 or distances[i] <= 0) {
          distances[i] = 0;
          Serial.println("Distance not in transmission range");
      } else {
        Serial.println(distances[i]);
      }
    }

}

void sendData(){

    //on 1st req, sends proximity sensor 1's distance
    if (state == 0) {
        Wire.write(distances[0]);
        state++;
    }
    //on 2nd req, sends a dummy number (for now)
    else if (state == 1){
        Wire.write(distances[1]);
        state++;
    } else if (state == 2) {
        Wire.write(distances[2]);
        state = 0;
    }

}

