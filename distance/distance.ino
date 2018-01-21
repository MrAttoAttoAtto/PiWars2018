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


volatile int state = 0;

byte echoPins[] = {7, 9, 11};
byte triggerPins[] = {8, 10, 12};
long durations[] = {0,0,0};
volatile int distances[] = {0,0,0};

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
    // Sets up echo inputs, and trigger outputs
    for (i=0;i<3;i++){
      pinMode(echoPins[i], INPUT);
      pinMode(triggerPins[i], OUTPUT);
    }

    

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
    Serial.println("---");
    for (i=0; i<3; i++) {
      digitalWrite(triggerPins[i], HIGH);
      delayMicroseconds(50);
      digitalWrite(triggerPins[i], LOW);
      durations[i] = pulseIn(echoPins[i], HIGH, 8000);
      distances[i] = durations[i] / 58.3;
      //makes distance 0 if it is a dodgy number
      if (distances[i] > 255 or distances[i] < 0) {
          distances[i] = 0;
          Serial.println("Distance not in transmission range");
      } else {
        Serial.println(distances[i]);
      }
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
    } else {
      for (i=0;i<strip.numPixels(); i++) {
        strip.setPixelColor(i, colour_options[colour]);
      }
      strip.show();
    }
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
