
#include <Servo.h>

Servo ServoX;

byte curr_deg;

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

void setup() {
  ServoX.attach(9);
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
    recvWithStartEndMarkers();
    showNewData();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {


   curr_deg = atoi(receivedChars);
      
      if(curr_deg >0 && curr_deg <=180)ServoX.write(curr_deg);
  
        Serial.println(receivedChars);
        newData = false;
    }
}
