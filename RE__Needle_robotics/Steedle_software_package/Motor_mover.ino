#include <AccelStepper.h>
#include <MultiStepper.h>

#include "SerialTransfer.h"
#include <SoftwareSerial.h>

SoftwareSerial HC05( A3, 13); //HC05-TX Pin 10, HC05-RX to Arduino Pin 11
SerialTransfer myTransfer;

#define M1_STEP_PIN         2
#define M1_DIR_PIN          5

#define M2_STEP_PIN         3
#define M2_DIR_PIN          6

#define M3_STEP_PIN         4
#define M3_DIR_PIN          7

#define ENABLE_PIN         8

AccelStepper stepperM1(1, M1_STEP_PIN, M1_DIR_PIN);
AccelStepper stepperM2(1, M2_STEP_PIN, M2_DIR_PIN);
AccelStepper stepperM3(1, M3_STEP_PIN, M3_DIR_PIN);

//Set empty arrays for the incoming steps
int step_count_M1[30];
int step_count_M2[30];
int step_count_M3[30];

//Assign stop_switches
int M1_switch = 9;       //Z-axis limit switch
int M2_switch = 10;      //Theta-axis limit switch
int M3_switch = 12;      //X-axis limit switch

char LED = LED_BUILTIN;
int counter = 0;
boolean M2H = false;
boolean Home = false;

MultiStepper steppers;

void setup()
{  
  HC05.begin(9600);
  myTransfer.begin(HC05);           //Start bluetooth communication

  //Enable the steppers
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);

  //Set max speed settings
  stepperM1.setMaxSpeed(500);
  stepperM2.setMaxSpeed(500);
  stepperM3.setMaxSpeed(500);

  //Set acc setting
  stepperM1.setAcceleration(3000);
  stepperM2.setAcceleration(3000);
  stepperM3.setAcceleration(3000);

  //stepperM1.setSpeed(500);

  //Add steppers to multi stepper
  steppers.addStepper(stepperM1);
  steppers.addStepper(stepperM2);
  steppers.addStepper(stepperM3);

  //Set up stop switches
  pinMode(M1_switch, INPUT_PULLUP);
  pinMode(M2_switch, INPUT_PULLUP);
  pinMode(M3_switch, INPUT_PULLUP);
  
  //stepperM3.move(3200);
  //stepperM3.runToPosition();
  
}

void loop(){
   if(myTransfer.available())
   {      
      uint16_t recSize = 0;

      //Put received data in assigened arrays
     for(int i=0; i < myTransfer.bytesRead/4; i++){
        if(counter == 0){
          myTransfer.rxObj( step_count_M1[i], recSize);
        }
        if(counter == 1){
          myTransfer.rxObj( step_count_M2[i], recSize);
        }
        if(counter == 2){
          myTransfer.rxObj( step_count_M3[i], recSize);
        }              
        recSize += 4;
     }
                   
     //Prepare buffer to be send back
     for(uint16_t i=0; i < myTransfer.bytesRead; i++){
        myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
     }
    //Send received array back to computer
    myTransfer.sendData(myTransfer.bytesRead);

    //Move the steppers if all arrays are filled
    if( counter == 2){
        counter = 0;

        //Check for go home command
        if( step_count_M1[0] == 28282 and step_count_M2[0] == 28282){
          GoHome();
        } 
        else{
          MoveEngines();
        }
    }
    else{
      counter +=1;    
    } 
   }      
}

void MoveEngines(){
   for(int i=0; i < myTransfer.bytesRead/4; i++){
    stepperM1.setCurrentPosition(0);
    stepperM2.setCurrentPosition(0);
    stepperM3.setCurrentPosition(0);

    stepperM1.setSpeed(1000);
  
    long positions[3] = {step_count_M1[i], step_count_M2[i], step_count_M3[i]};
      
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
    //delay(1000);
   }
}

void GoHome(){
  if(Home == false){
   while(true)
     {    
         int counter = 0;
         stepperM1.setSpeed(-500);
         stepperM2.setSpeed(500);
         stepperM3.setSpeed(-800);

         if(digitalRead(M1_switch) == HIGH){
          stepperM1.stop();
          
          counter += 1;
         }    
         else{
          stepperM1.runSpeed();
         }
         
         if(digitalRead(M2_switch) == HIGH or M2H == true){
          stepperM2.stop();
          M2H = true;
          counter += 1;
         }
         else{
          stepperM2.runSpeed();
         }
         
         if(digitalRead(M3_switch) == HIGH){
          stepperM3.stop();
          counter += 1;
         }
         else{
          stepperM3.runSpeed();
         }
      
         if(counter == 3){
          Home = true;
          break;
         }                      
     }

   //Move to starting position
   Home = false;
   delay(1000);
   stepperM1.setCurrentPosition(0);
   stepperM2.setCurrentPosition(0);
   stepperM3.setCurrentPosition(0);

   //Steps to home position from stop switch
   int M1_dis = step_count_M1[1];
   int M2_dis = step_count_M2[1];
   int M3_dis = step_count_M3[1];
   
   stepperM1.move(M1_dis);
   stepperM2.move(M2_dis);
   stepperM3.move(M3_dis);
   M2H = false;
      
   while(true) 
   { 
      stepperM1.setSpeed(500);
      stepperM2.setSpeed(-500);
      stepperM3.setSpeed(800);
      int counter = 0;
      if (stepperM1.distanceToGo()){
       stepperM1.run();
       counter +=1;
      }
      if (stepperM2.distanceToGo()){
       stepperM2.run();
       counter +=1;
      }
      if (stepperM3.distanceToGo()){
       stepperM3.run();
       counter +=1;
      }
      if (counter == 0){
        Serial.print(counter); 
        break;
      }
   }
  } 
}

   
