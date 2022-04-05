/*
CONNECTIONS:

GND........GND
VCC........5V
R_EN.......5V
L_EN.......5V
RPWM.......D5
LPWM.......D6






*/

#define FWD 5
#define BWD 6

void setup(){
pinMode(FWD, OUTPUT);
pinMode(BWD, OUTPUT);
}
void loop(){

analogWrite(FWD, 155);
analogWrite(BWD, 0);
  delay(2000);
analogWrite(BWD, 155);
analogWrite(FWD, 0);
  delay(2000);
}
