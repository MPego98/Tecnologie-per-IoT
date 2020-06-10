#include <TimerOne.h>


#include <LiquidCrystal_PCF8574.h>
LiquidCrystal_PCF8574 lcd(0x27);
#define n_step 10
#define screen_rot 4 //expressed in second
#define presence_numS 50
#define event_time 1// expressed in minutes
#define B 4275
#define  R0 100000
#define wait_time 2000

#define min_clap 250
#define max_clap 700
//fan
const int Fan_Pin= 13;
float Tac_min_abs=24.0,Tac_min_pres=20.0,Tac_max_abs=30.0,Tac_max_pres=26.0,Tac_Max,Tac_Min;
float fan_speed=0;
//temperature sensor
const int Temp_Pin= A1;


//heater
const int Heat_Pin= 12;
float The_min_abs=115.0,The_min_pres=16.0,The_max_abs=17.0,The_max_pres=19.0,The_Max,The_Min;
float heat_pow=0;
//sound
const int Sound_Pin= 7;
volatile long int counterS=0;
int timeout_Sound=1;//expressed in minutes
bool presenceS=false;
volatile int counter_event=0;
int MobileBlock[event_time];
int abs_time=0; //rapresente the number of time that for "time_event" minute the is not enought sound
volatile long int wait=0;
//pir
const int Pir_Pin= 8;
volatile long int counterP=0;
int timeout_Pir=1;
bool presenceP=false;
volatile int counter_eventP=0;
//screen
volatile int ScreenC=0;
int ScreenStatus=1;
//light
const int Light_Pin = 6;
volatile bool clapped=0;
volatile int wait_L=0;
volatile int LightState=LOW;






void setup() {
  Timer1.initialize(1 *1e6);
  Timer1.attachInterrupt(Update_Stat);
  //lcd set
  lcd.begin(16,2);
  lcd.setBacklight(150);
  lcd.home();
  lcd.clear();
 
  
  //fan set
  pinMode(Fan_Pin,OUTPUT);
 analogWrite(Fan_Pin,0);
  //heater set
  pinMode(Heat_Pin,OUTPUT);
 analogWrite(Heat_Pin,0);
  //temperature set
  pinMode(Temp_Pin,INPUT);
  //sound set
  pinMode(Sound_Pin,INPUT);
  attachInterrupt(digitalPinToInterrupt(Sound_Pin),LightUp,RISING);
  //Pir set
  pinMode(Pir_Pin,INPUT);
  //Serial set
   lcd.write("Starting ...");
   lcd.setCursor(0,1);
   lcd.write("Open Serial");
  Serial.begin(9600);
  while(!Serial);
 Serial.println("insert the data  Heater/Fan Max/Min Presence/Absence temperature with the encoding H = heater, F= Fan, MAX= Max, MIN= Min, P = presence, A= Absence" );
 Serial.println("for example i would change the minimum temperature of fan when there is sameone i have to write F MIN P 24.3");
 
 
  //Writing Temperature Parameter
  //StartParameter();
  Tac_Max=Tac_max_abs;
  Tac_Min=Tac_min_abs;
  The_Max=The_max_abs;
  The_Min=The_min_abs;
  //Serial.println("started");
}
void serialEvent() {
  String readed=Serial.readString();
  readed.toUpperCase();
  bool end_=false;
  bool error=false;
  int state=0;
  int counter=0;
  String Result;
  float temperature;
  while(!end_ && !error)
  {
    switch(state)
    {
      case 0://read type( H= heater, F= fan)
      {
        state=1;
        if(readed.charAt(counter)=='H')
          Result="1";
        else if(readed.charAt(counter)=='F')
          Result="0";
        else if(readed.charAt(counter)==' ')
        {
          state=0;
        }
        else
          error=true; 
        counter++;  
      }break;
      case 1://read if max or min
      {
        state=2;
        if(readed.charAt(counter)==' ')
        {
          state=1;
          counter ++;
        } 
        else
        {
          if(readed.substring(counter,counter+3)=="MAX")
            Result+="1";
          else if(readed.substring(counter,counter+3)=="MIN")
            Result+="0";
          else
            error=true;
           counter+=4;  
      
        }
      }break;
      case 2://read presence/absence( P= presence, A= absence)
      {
        state=3;
        if(readed.charAt(counter)=='P')
          Result+="1";
        else if(readed.charAt(counter)=='A')
          Result+="0";
        else if(readed.charAt(counter)==' ')
        {
          state=2;
        }
        else
          error=true; 
        counter++;  
     
      }break;
      case 3://read if max or min
      {
        state=4;
        if(readed.charAt(counter)==' ')
        {
          state=3;
          counter ++;
        } 
        else
        {
          String tmp;
          if(readed.charAt(counter)=='-')
          {
            temperature=-1;
             tmp =readed.substring(counter+1,counter+5);
          }
          else
          { 
            temperature=1;
            tmp =readed.substring(counter,counter+4);
          }
     
          if(isDigit(tmp[0]) && isDigit(tmp[1]) && isDigit(tmp[3]))
          {
            temperature=temperature*tmp.toFloat();
      
            if(temperature>99 || temperature < -99  )
              error=true;
            else
             end_=true;
          }
          else
            error=true;
        }
      }break;     
    }
  }
  if(!error)
  {
    StartParameter(Result.toInt(),temperature);
    Serial.println("parameter changed");
  }
  else
    Serial.println("wrong parameter");
 Serial.println("insert the data  Heater/Fan Max/Min Presence/Absence temperature with the encoding H = heater, F= Fan, MAX= Max, MIN= Min, P = presence, A= Absence" );
 Serial.println("for example i would change the minimum temperature of fan when there is sameone i have to write F MIN P 24.3");
 
}
void StartParameter(int result,float temperature)
{
  switch(result)
  {
     case 1: Tac_min_pres=temperature;break;

      case 11:Tac_max_pres=temperature;break;

      case 0:Tac_min_abs=temperature;break;

      case 10:Tac_max_abs=temperature;break;

     case 101: The_min_pres=temperature;break;

     case 111: The_max_pres=temperature;break;

      case 100:The_min_abs=temperature;break;
   
     case 110: The_max_abs=temperature;break;
  }
 
}

float ReadTemperature()
{
  int a = analogRead(Temp_Pin);

    float R = 1023.0/a-1.0;
    R = R0*R;
   float temperature = (1.0/((log(R/R0)/B)+(1/298.15)))-273.15; // convert to temperature via datasheet
 return temperature;
}
/*
void CheckPresenceS()
{
  
  if(millis()-wait>wait_time)
  {
    counter_event=counter_event +1;
    Serial.println(millis()-wait);
    Serial.println(counter_event);
    wait=millis();
  }
    
}
*/
void LightUp()
{
  if(clapped)
  {
    int passed=millis()-wait_L;
    if(passed>min_clap)
    {
      if(passed<max_clap)
      {
        LightState=!LightState;
        digitalWrite(Light_Pin,LightState);
        clapped=false;
      }
      else
      { 
        clapped=true;
        wait_L=millis();
      }
    }
  }
  else
  { 
    wait_L=millis();
    clapped=true;
  }
  
}
void CheckPresenceP()
{
  if(digitalRead(Pir_Pin)==HIGH)
  {
    counter_eventP=1;
    counterP=0;
  }
 
}

void Update_Stat()
{
  counterS=counterS+1;
  counterS=counterS+1;
  ScreenC=ScreenC+1;
}
void mooveFan(float step_pos)
{

  fan_speed=step_pos*255/n_step;
  if(fan_speed>255)
    fan_speed=255;

   
 analogWrite(Fan_Pin,(int)fan_speed);
}

void HeaterOn(float step_pos)
{
  heat_pow=step_pos*255/n_step;
  if( heat_pow>255)
     heat_pow=255;
  analogWrite(Heat_Pin,(int) heat_pow);
}

void UpdateScreen(float Temp)
{
  if(ScreenC>screen_rot)
  {
    ScreenC=0;
    ScreenStatus= !ScreenStatus;
    if(ScreenStatus)
    {
      lcd.home();
      lcd.clear();
      lcd.write("AC m:");
      lcd.print(Tac_Min);
      lcd.setCursor(9,0);
      lcd.write(" M:");
      lcd.print(Tac_Max);
      lcd.setCursor(0,1);
      lcd.write("HE m:");
      lcd.print(The_Min);
      lcd.setCursor(9,1);
      lcd.write(" M:");
      lcd.print(The_Max);
    }
    else
    {
      lcd.home();
      lcd.clear();
      lcd.write("T:");
      lcd.print(Temp);
      lcd.setCursor(8,0);
      lcd.write(" Pres: ");
      lcd.print(presenceP||presenceS);
      lcd.setCursor(0,1);
      lcd.write("FA:");
      lcd.print(int(fan_speed*100/255));
      lcd.write("%  HE: ");
      lcd.print(int(heat_pow*100/255));
      lcd.write("%");
    }
  }
  
}
void loop() {
  CheckPresenceP();
  if(counterP<timeout_Pir*60 )// check pir presence
      presenceP=true;
  else
      presenceP=false;
  
     
/*this part control if there are people based on the sound sensor*/
/* if(counterS>60 )// check if one minutes is passed
   {
    int sum=0;
    for(int i =event_time-1;i>=0;i--)
    {
      MobileBlock[i]=MobileBlock[i-1];//shift of the mobile block register
      sum=sum+MobileBlock[i-1];
    }
    MobileBlock[0]=counter_event;
    sum=sum+counter_event;
    if(sum<presence_numS)
        abs_time++;
    else
        abs_time=0;
    if(abs_time>timeout_Sound)
        presenceS=false;
    else
        presenceS=true;
    counter_event=0;
    counterS=0;
  }*/
  if(/*presenceS || */presenceP)// determinate if there is sameone
  {
    Tac_Max=Tac_max_pres;
    Tac_Min=Tac_min_pres;
    The_Max=The_max_pres;
    The_Min=The_min_pres;
  }
  else
  {
    Tac_Max=Tac_max_abs;
    Tac_Min=Tac_min_abs;
    The_Max=The_max_abs;
    The_Min=The_min_abs;
  }
  float temp=ReadTemperature();
  //Serial.println(temp);
  if(temp>Tac_Min)
  {
    mooveFan((temp-Tac_Min)*((Tac_Max-Tac_Min)/n_step));
  }
  else
    mooveFan(0);
   if(temp<The_Max)
  {
   HeaterOn((The_Max-temp)*((The_Max-The_Min)/n_step));
  }
  else
    HeaterOn(0);
  UpdateScreen(temp);
if (Serial.available()>0)
{
  serialEvent();
  Serial.flush();
}

}
