#define B 4275
#define  R0 100000
#include <TimerOne.h>
const int Temp_Pin= A1;

void setup() {
  pinMode(Temp_Pin,INPUT);
 
  Timer1.initialize(10 *1e6);
  Timer1.attachInterrupt(print_status);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Lab 1.5 starting");
  
}
float ReadTemperature()
{
  int a = analogRead(Temp_Pin);

    float R = 1023.0/a-1.0;
    R = R0*R;
   float temperature = (1.0/((log(R/R0)/B)+(1/298.15)))-273.15; // convert to temperature via datasheet
 return temperature;
}
void print_status()
{
  Serial.print("Temperature: ");
  Serial.println(String(ReadTemperature())+" C");
}
void loop() {
 

}
