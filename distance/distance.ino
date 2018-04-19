#include <NewPing.h>

int distance;


#define MAX_DISTANCE 255
NewPing sonarleft(8, 7, MAX_DISTANCE);
NewPing sonarmiddle(10, 9, MAX_DISTANCE);
NewPing sonarright(12, 11, MAX_DISTANCE);

NewPing sonars[] = {sonarleft, sonarmiddle, sonarright};

void setup()
{
  //Just for checking
  Serial.begin(9600);
}

//Continously gets a distance reading, modifiying it if it is not ok
void loop()
{
  if (Serial.available()) {
    
    byte i = Serial.read();
    distance = sonars[i].ping_cm();
    
    if (distance > 255)
    {
      distance = 255;
    } else if (distance <= 0) {
      distance = 0;
    }
    Serial.write(distance);
  }
}
