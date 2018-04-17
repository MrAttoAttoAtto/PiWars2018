/*
WIRING:
-------------------------------------------
  I2C
-------------------------------------------
  NANO USB -> PI USB
-------------------------------------------
  DISTANCE SENSOR 1
-------------------------------------------
  GND -----> GND
  VCC -----> +5V

  ECHO -----> D7
  TRIG -----> D8
 
 */

byte echoPins[] = {7, 9, 11};
byte triggerPins[] = {8, 10, 12};
long duration;
int distance;
uint16_t i;

void setup()
{
  // Sets up echo inputs, and trigger outputs
  for (i = 0; i < 3; i++)
  {
    pinMode(echoPins[i], INPUT);
    pinMode(triggerPins[i], OUTPUT);
  }

  //Just for checking
  Serial.begin(9600);
}

//Continously gets a distance reading, modifiying it if it is not ok
void loop()
{
  if (Serial.available()) {
    byte i = Serial.read();
    digitalWrite(triggerPins[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPins[i], LOW);
    duration = pulseIn(echoPins[i], HIGH, 16000);
    distance = duration / 58;
    //makes distance 0 if it is a dodgy number

    if (distance > 255)
    {
      distance = 255;
    } else if (distance <= 0) {
      distance = 0;
    }
    Serial.write(distance);
  }
}