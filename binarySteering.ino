
/*
  CONNECTIONS:

  GND........GND
  VCC........5V
  R_EN.......5V
  L_EN.......5V
  RPWM.......D5
  LPWM.......D6
  Servo......D9

Driver Voltage:  5 V

min. PWM: 140

*/

#define FWD1 9

#define FWD2 10

#define DEL 1000

byte rec;

bool mot = 0;

const byte numChars = 8;

char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char messageFromPC[numChars] = {0};
byte rec1 = 0;
byte rec2 = 0;

//time related
unsigned long currMillis;
unsigned long lastMillis = 0;


byte left = 0;
byte right = 0;

boolean newData = false;

//============

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  for (byte i = 3; i < 11; i++)pinMode(i, OUTPUT);

 }

//============

void loop() {
  currMillis = millis();
  recvWithStartEndMarkers();
  confirmData();

}



//============

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



void parseData() {      // split the data into its parts

  char * strtokIndx; // this is used by strtok() as an index

  strtokIndx = strtok(tempChars, "*");     // get the first part - the string
  strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
  rec1 = atoi(strtokIndx);

  strtokIndx = strtok(NULL, "*"); // this continues where the previous call left off
  rec2 = atoi(strtokIndx);     // convert this part to an integer

  left = rec1;
  right = rec2;

}



void showParsedData() {
  Serial.print("left ");
  Serial.print(left);

  Serial.print(" right ");
  Serial.print(right);
  Serial.println(" ");

  analogWrite(FWD1, left);
  analogWrite(FWD2, right);

}

void confirmData() {
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    parseData();
    showParsedData();
    newData = false;
  }



}
