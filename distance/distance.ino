#include <Wire.h>
#include <Adafruit_NeoPixel.h>

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
#define NEOPIN 6
#define echo1 7
#define trig1 8

#define echo2 9
#define trig2 10

int state = 0;

long distance1;
long distance2;
int duration1;
int duration2;
long distance;
int duration;
volatile byte colour;
uint16_t i;
uint16_t j = 0;

 
// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(8, NEOPIN, NEO_GRB + NEO_KHZ800);
uint32_t colour_options[] = {strip.Color(0,0,0), strip.Color(255, 0, 0), strip.Color(0, 255, 0), strip.Color(0, 0, 255), strip.Color(255, 0, 255)};



void setup() {
    //Sets up pins for ultrasonic tingz
    pinMode(echo1, INPUT);
    pinMode(trig1, OUTPUT);

    pinMode(echo2, INPUT);
    pinMode(trig2, OUTPUT);

    //Just for checking
    Serial.begin(9600);
    Serial.println("Ready!");

    strip.begin();
    strip.show(); // Initialize all pixels to 'off'


    //Initializes i2c and has a function run whenver a request comes in
    Wire.begin(SLAVE_ADDRESS);
    Wire.onRequest(sendData);
    Wire.onReceive(receiveEvent); // register event
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
    if (colour == 5) {
      j++;
      for(i=0; i< strip.numPixels(); i++) {
        strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
      }
      strip.show();
      if (j == 256) {
        j = 0;
      }
    }
    strip.setPixelColor(0, colour_options[colour]);
    strip.show();
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  byte x;
  while (Wire.available()) {
      x = Wire.read();
  }
  colour = x;
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


// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
