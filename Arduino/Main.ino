//-------------------------------------------------------- Libraries --------------------------------------------------------------------------
#include <Servo.h>

//----------------------------------------------------- Value constants -----------------------------------------------------------------------
#define BAUD_RATE 9600
#define BLDC_FWD_H 1900
#define BLDC_FWD_M 1700
#define BLDC_FWD_L 1600
#define BLDC_BACKWD_H 1100
#define BLDC_BACKWD_M 1300
#define BLDC_BACKWD_L 1400
#define BLDC_STOP 1500
#define BLDC_ARMING_DELAY 5000 //this value may need to be adjusted
#define CURRENT_SENSOR_SCALE_FACTOR 185 //mV/A

//--------------------------------------------------- Pin number constants ---------------------------------------------------------------------
#define BLDC1_PIN 9
#define BLDC2_PIN 10
#define R_MOTOR_PIN1 4
#define R_MOTOR_PIN2 5
#define L_MOTOR_PIN1 7
#define L_MOTOR_PIN2 8
#define SERVO_PIN 3
#define DIFF_LED_PIN A0
#define SPEED_LED1_PIN A3
#define SPEED_LED2_PIN A2
#define SPEED_LED3_PIN A1
#define DIFF_BUZZER_PIN 12
#define VOLTMETER_PIN A7
#define CURRENT_PIN A5
#define LEAKAGE_PIN A6

int OUTPUTS[] = {R_MOTOR_PIN1, R_MOTOR_PIN2, L_MOTOR_PIN1, L_MOTOR_PIN2, DIFF_LED_PIN, DIFF_BUZZER_PIN};
int INPUTS[] = {VOLTMETER_PIN, CURRENT_PIN, LEAKAGE_PIN};

//--------------------------------------------------- State and data variables ---------------------------------------------------------------------
String guiData; //a string to hold the data coming from the GUI
char rMotorState = 'C', lMotorState = 'C', motorType = 'D', motorSpeed = 'L'; //the initial states of the motors and variables
int differences = 0, angle = 0;
float voltmeter_reading = 0;
float current_reading = 0;

//--------------------------------------------------- Servos and BLDCs ----------------------------------------------------------------------------
Servo bldc1;
Servo bldc2;
Servo servo;

//--------------------------------------------------- function prototypes --------------------------------------------------------------------------
void updateStates();
void motorControl(char type, char dir1, char dir2, char spd);
void armBLDC(int delayVal);
float voltmeter();
float currentmeter();
void sendData(float voltmeter, float current, float leakage);

void setup()
{
//--------------------------------------------------- Assigning data direction for pins -----------------------------------------------------------
  for(int i = 0 ; i < 6 ; i++) pinMode(OUTPUTS[i], OUTPUT);
  for(int i = 0 ; i < 3 ; i++) pinMode(INPUTS[i], INPUT);

//------------------------------------------------------ Initialize pin states -------------------------------------------------------------------
  for(int i = 0 ; i < 6 ; i++) digitalWrite(OUTPUTS[i], LOW);

//---------------------------------------------------- Attach the Servo and BLDC pins --------------------------------------------------------------
  bldc1.attach(BLDC1_PIN);
  bldc2.attach(BLDC2_PIN);
  servo.attach(SERVO_PIN);

//-------------------------------------------------------- Arming the BLDC motors ------------------------------------------------------------------
  armBLDC(BLDC_ARMING_DELAY);

//------------------------------------------------------- Begin a serial connection -----------------------------------------------------------------
  Serial.begin(BAUD_RATE);
}

void loop()
{
  //updateStates();
  //motorControl(motorType, rMotorState, lMotorState, motorSpeed);
  digitalWrite(R_MOTOR_PIN1, HIGH);
  digitalWrite(R_MOTOR_PIN2, HIGH);
  digitalWrite(L_MOTOR_PIN1, LOW);
  digitalWrite(L_MOTOR_PIN2, LOW);
  servo.write(0);
  delay(1000);
  servo.write(180);
  //voltmeter_reading = voltmeter();
  //current_reading = currentmeter()
  //sendData(voltmeter_reading, current_reading, analogRead(LEAKAGE_PIN));
}

//----------------------------------------recieve the data from the GUI and update the state variables-----------------------------------------------
void updateStates() 
{
  if (Serial.available() > 0)
  {
    guiData = Serial.readString(); //read the data string coming from the GUI
    //parse the data into their desired state variables
    motorType = guiData[0];
    motorSpeed = guiData[1];
    rMotorState = guiData[2];
    lMotorState = guiData[3];
    differences = (guiData[4] - '0');
    angle = ( (guiData[5] - '0') * 100 + (guiData[6] - '0') * 10 + (guiData[7] - '0') );
  }
}

//------------------------------------------------------------control the motors---------------------------------------------------------------------
void motorControl(char type, char dir1, char dir2, char spd) 
{
  int bldcSignals[2];
  if(spd == 'L')
  {
    bldcSignals[0] = BLDC_FWD_L;
    bldcSignals[1] = BLDC_BACKWD_L;
    digitalWrite(SPEED_LED1_PIN, HIGH);
    digitalWrite(SPEED_LED2_PIN, LOW);
    digitalWrite(SPEED_LED3_PIN, LOW);
  }
  else if(spd == 'M')
  {
    bldcSignals[0] = BLDC_FWD_M;
    bldcSignals[1] = BLDC_BACKWD_M;
    digitalWrite(SPEED_LED1_PIN, HIGH);
    digitalWrite(SPEED_LED2_PIN, HIGH);
    digitalWrite(SPEED_LED3_PIN, LOW);
  }
  else if(spd == 'H')
  {
    bldcSignals[0] = BLDC_FWD_H;
    bldcSignals[1] = BLDC_BACKWD_H;
    digitalWrite(SPEED_LED1_PIN, HIGH);
    digitalWrite(SPEED_LED2_PIN, HIGH);
    digitalWrite(SPEED_LED3_PIN, HIGH);
  }
  
  if(type == 'D') //if it's a dc motor
  {
    //stop the BLDC motors
    bldc1.writeMicroseconds(BLDC_STOP);
    bldc2.writeMicroseconds(BLDC_STOP);
    
    if(dir1 == 'C')
    {
      digitalWrite(R_MOTOR_PIN1, HIGH);
      digitalWrite(R_MOTOR_PIN2, HIGH);
    }
    else if(dir1 == 'A')
    {
      digitalWrite(R_MOTOR_PIN1, LOW);
      digitalWrite(R_MOTOR_PIN2, LOW);
    }
    else if(dir1 == 'S')
    {
      digitalWrite(R_MOTOR_PIN1, HIGH);
      digitalWrite(R_MOTOR_PIN2, LOW);
    }

    if(dir2 == 'C')
    {
      digitalWrite(L_MOTOR_PIN1, HIGH);
      digitalWrite(L_MOTOR_PIN2, HIGH);
    }
    else if(dir2 == 'A')
    {
      digitalWrite(L_MOTOR_PIN1, LOW);
      digitalWrite(L_MOTOR_PIN2, LOW);
    }
    else if(dir2 == 'S')
    {
      digitalWrite(L_MOTOR_PIN1, HIGH);
      digitalWrite(L_MOTOR_PIN2, LOW);
    }
  }
  
  else if(type == 'B') //if it's a brushless motor
  {
    //Stop the DC motors
    digitalWrite(L_MOTOR_PIN1, HIGH);
    digitalWrite(L_MOTOR_PIN2, LOW);
    digitalWrite(R_MOTOR_PIN1, HIGH);
    digitalWrite(R_MOTOR_PIN2, LOW);
    
    if(dir1 == 'C') bldc1.writeMicroseconds(bldcSignals[0]);
    else if(dir1 == 'A')  bldc1.writeMicroseconds(bldcSignals[1]);
    else if(dir1 == 'S')  bldc1.writeMicroseconds(BLDC_STOP);

    if(dir2 == 'C') bldc2.writeMicroseconds(bldcSignals[0]);
    else if(dir2 == 'A')  bldc2.writeMicroseconds(bldcSignals[1]);
    else if(dir2 == 'S')  bldc2.writeMicroseconds(BLDC_STOP);
  }
  
}

//----------------------------------------------------------Arm the BLDC motors----------------------------------------------------------------------
void armBLDC(int delayVal)
{
  bldc1.writeMicroseconds(BLDC_STOP);
  bldc2.writeMicroseconds(BLDC_STOP);
  delay(delayVal); 
  
}

//------------------------------------------indicate the number of differences found in the 2 images----------------------------------------------------
void showDiff()
{
  for(int i = 0 ; i < differences ; i++)
  {
    digitalWrite(DIFF_LED_PIN, HIGH);
    digitalWrite(DIFF_BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(DIFF_LED_PIN, LOW);
    digitalWrite(DIFF_BUZZER_PIN, LOW);
  }
}

//----------------------------------------------Verifies the voltage of the power supply-------------------------------------------------------------------
float voltmeter()
{
  float reading = analogRead(VOLTMETER_PIN);
  float voltage = map(reading, 0, 1023, 0, 55);
  return voltage;
}

//-----------------------------------------------Calculate the supply current draw------------------------------------------------------------------------
float currentmeter()
{
  float reading = analogRead(CURRENT_PIN);
  float millivolts = (reading / 1023 )* 5000;
  float current = (millivolts - 2500) / CURRENT_SENSOR_SCALE_FACTOR;
  return current;
}
//---------------------------------------------------Sends the sensor data to the GUI---------------------------------------------------------------------
void sendData(float voltmeter, float current, float leakage)
{
  String data = (String)voltmeter + " " + (String)current + " " + (String)leakage;
  Serial.println(data);
}
