#include <Wire.h>

#define echoPin1 7
#define echoPin2 9
#define trigPin1 8
#define trigPin2 10

int triggers[3] = { 2, 4, 6 };
int echos[3] = { 3, 5, 7 };

long duration1, distance1;
long duration2, distance2;


void setup() {
  
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
  int i = 0;
  for (i=0;i<3;i++) {
    pinMode(triggers[i], OUTPUT); 
  }
  for (i=0;i<3;i++) {
    pinMode(echos[i], INPUT); 
  }
}

void loop() {
  delay(100);
}


void requestEvent() {
  int noodles[3];
  for (int i = 0;i<3;i++){
    noodles[i] = measure_distance(i);
  }
  Wire.write(noodles, 12);
  
}

long measure_distance(int id) {
  digitalWrite(triggers[id], LOW);
  delayMicroseconds(2);
  digitalWrite(triggers[id], HIGH);
  delayMicroseconds(10);
  digitalWrite(triggers[id], LOW);
  int duration = pulseIn(echos[id], HIGH);
  return duration/58.2;
}

