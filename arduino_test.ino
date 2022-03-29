#define FWD 5
#define BWD 6
#define L_EN 7
#define R_EN 8

#define DEL 1000


const byte pwmMin = 20;
const byte pwmMax = 255;
const byte numChars = 8;
byte PWM = 0;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char messageFromPC[numChars] = {0};
int rec1 = 0;
int rec2 = 0;

//time related
unsigned long currMillis;
unsigned long lastMillis = 0;



boolean newData = false;

//============

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
    pinMode(FWD, OUTPUT);
    pinMode(BWD, OUTPUT);
    analogWrite(FWD, 0);
    analogWrite(BWD, 0);

    digitalWrite(L_EN, 1);
    digitalWrite(R_EN, 1);
    
    }

//============

void loop() {
    currMillis = millis();
    recvWithStartEndMarkers();
    confirmData();
    
    if(currMillis - lastMillis >= DEL){
    driveMotor();
    lastMillis = currMillis;
    }
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

    strtokIndx = strtok(tempChars,"*");      // get the first part - the string
    strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
    rec1 = atoi(strtokIndx);
 
    strtokIndx = strtok(NULL, "*"); // this continues where the previous call left off
    rec2 = atoi(strtokIndx);     // convert this part to an integer


}


void showParsedData() {
    Serial.print("rec1: ");
    Serial.print(rec1);
   // Serial.print("rec2: ");
    //Serial.print(rec2);

}

void confirmData(){
  if (newData == true) {
        strcpy(tempChars, receivedChars);
        parseData();
        showParsedData();
        newData = false;
    }
  }

void driveMotor(){
  
if(analogRead(FWD)!=0) analogWrite(BWD, 0);
else if (analogRead(BWD)!=0) analogWrite(FWD, 0);


byte speedMot = abs(90-rec1);
PWM = map(speedMot ,0, 90, pwmMax, pwmMin);
analogWrite(FWD, PWM);
Serial.println("FWD PWM ");
Serial.print(PWM);


  }


  
