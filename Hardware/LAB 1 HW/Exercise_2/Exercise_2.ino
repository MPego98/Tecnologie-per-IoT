#include <TimerOne.h> 

const int RLED_PIN = 12;
const int GLED_PIN = 13;

const float R_HALF_PERIOD = 1.5;
const float G_HALF_PERIOD = 3.5;

int greenLedState = LOW;
int redLedState = LOW;


volatile int ledPinValueRed,ledPinValueGreen;

void blinkGreen(){
  greenLedState = !greenLedState;
  digitalWrite(GLED_PIN, greenLedState);
 
}

void serialPrintStatus(){
  
 
}


void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Lab 1.2 Starting");
  
  pinMode(RLED_PIN, OUTPUT);
  pinMode(GLED_PIN, OUTPUT);
 
  Timer1.initialize(G_HALF_PERIOD *1e06); //genera un interrupt ogni tot secondi
  Timer1.attachInterrupt(blinkGreen);

   //attachInterrupt(Serial.read(), inter_PIR, CHANGE);
  

}

void loop() {
 redLedState = !redLedState;
 digitalWrite(RLED_PIN, redLedState);  
 
 delay(R_HALF_PERIOD *1e03);



 



}



void serialEvent() 
{
  ledPinValueRed = digitalRead(RLED_PIN);
  ledPinValueGreen = digitalRead(GLED_PIN);
  if (Serial.available())
  {
    char ch = Serial.read();
    if (ch == 'R')
    {
      Serial.print("LED Rosso: ");
     Serial.println(ledPinValueRed);
     
    }else if (ch == 'G') {
      Serial.print("LED Verde: ");
     Serial.println(ledPinValueGreen);
    }else{
      Serial.println("Invalid Command");
    }

    
  }

}
