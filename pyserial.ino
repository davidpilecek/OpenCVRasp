#define DELAY 10


#include <Servo.h>

Servo ServoX;

byte deg;
byte rec;
byte ang;
byte lastDeg = 0;
byte currDeg;

unsigned long curr_millis;
unsigned long last_millis = 0;

byte last_deg = 0;
byte curr_deg;

void setup() {

  ServoX.attach(9);
  Serial.begin(115200);
  Serial.setTimeout(1);

}

void loop() {
  curr_millis = millis();
  
  while (!Serial.available());

  curr_deg = Serial.readString().toInt();

  ServoX.write(curr_deg);
  Serial.print(curr_deg);
 delay(5);

}
