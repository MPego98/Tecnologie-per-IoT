#define B 4275
#define  R0 100000
#include <TimerOne.h>
#include <LiquidCrystal_PCF8574.h>
LiquidCrystal_PCF8574 lcd(0x27);
const int Temp_Pin= A1;

void setup() {
  pinMode(Temp_Pin,INPUT);
 
  Timer1.initialize(10 *1e6);
  Timer1.attachInterrupt(print_status);
 lcd.begin(16,2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
  lcd.write("Temperature:");
 
  
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
  lcd.setCursor(12,0);
  lcd.write(ReadTemperature());
}
void loop() {
 

}
