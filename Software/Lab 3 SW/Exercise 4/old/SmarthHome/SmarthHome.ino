#include <TimerOne.h>
#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <Process.h>
#include <ArduinoJson.h>
#include <MQTTclient.h>
#include <LiquidCrystal_PCF8574.h>
LiquidCrystal_PCF8574 lcd(0x27);
#define n_step 10
#define screen_rot 4 //expressed in second
#define presence_numS 50
#define event_time 1// expressed in minutes
#define B 4275
#define  R0 100000
#define wait_time 2000
#define Temp_Pin A1
#define Heat_Pin 12
#define Sound_Pin 7
#define Pir_Pin 8
#define Led_Pin 4
#define timeout_Sound 1
#define timeout_Pir 1
#define Fan_Pin 13
int tim=0,tim1=0;
//fan

float Tac_min_abs=20.0,Tac_min_pres=28.0,Tac_max_abs=30.0,Tac_max_pres=30.0,Tac_Max,Tac_Min;

//temperature sensor



//heater

float The_min_abs=15.0,The_min_pres=14.0,The_max_abs=17.0,The_max_pres=28.0,The_Max,The_Min;

//sound

volatile int counterS=0;
//expressed in minutes
volatile bool presenceS=false;
volatile int counter_event=0;
int MobileBlock[event_time];
int abs_time=0; //rapresente the number of time that for "time_event" minute the is not enought sound
volatile  int wait=0;
//pir

volatile  int counterP=0;

volatile bool presenceP=false;
volatile int counter_eventP=0;
//screen


//light






String heartbit;
 const int capacity= JSON_OBJECT_SIZE(3)+JSON_ARRAY_SIZE(5)+JSON_OBJECT_SIZE(5)+40;
  DynamicJsonDocument doc_rec(capacity);
  DynamicJsonDocument doc_snd(capacity);
void setup() {
  pinMode(Led_Pin, OUTPUT);
  Serial.begin(9600);
  while(!Serial);
 
  Serial.println("starting...");

 pinMode(LED_BUILTIN, OUTPUT);
 
  digitalWrite(LED_BUILTIN,LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN,HIGH);
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
  attachInterrupt(digitalPinToInterrupt(Sound_Pin),CheckPresenceS,RISING);
  //Pir set
  pinMode(Pir_Pin,INPUT);
  //Serial set

 
  mqtt.begin("test.mosquitto.org",1883);
  mqtt.subscribe("tiot/17/home/light",setLedValue);
  mqtt.subscribe("tiot/17/home/screen",setScreenValue);

  //Writing Temperature Parameter
  //StartParameter();
  Tac_Max=Tac_max_abs;
  Tac_Min=Tac_min_abs;
  The_Max=The_max_abs;
  The_Min=The_min_abs;
  Serial.println("started");
 /* doc_snd.clear();
  doc_snd["ID"]="Yun";
  doc_snd["endPoint"]="tiot/17/home/";
  JsonArray data = doc_snd.createNestedArray("avaibleResources");
  data.add("led");
  data.add("temperature");
  data.add("screen");
  data.add("presence");
  data.add("noise");

  serializeJson(doc_snd, heartbit);
  delay(1000);
  Serial.println(doc_snd.memoryUsage());*/
  heartbit=F("{\"ID\":\"Yun\",\"endPoint\":\"tiot/17/home\",\" avaibleResources\":[\"led\",\"temperature\",\"screen\",\"presnece\",\"noise\"]}");
}


void setLedValue(const String& topic, const String& subtopic, const String& message)
{
  DeserializationError err = deserializeJson(doc_rec,message);
  if(err)
  {
    Serial.print(F("deserializedJson failed with code"));
    Serial.println(err.c_str());
  }else
  if( doc_rec["e"][0]["n"]=="led")
  {
    int val=doc_rec["e"][0]["v"];
    if(val==1||val==0)
    {
      digitalWrite(Led_Pin,val);
    }
  }
}
void setScreenValue(const String& topic, const String& subtopic, const String& message)
{
  DeserializationError err = deserializeJson(doc_rec,message);
  if(err)
  {
    Serial.print(F("deserializedJson failed with code"));
    Serial.println(err.c_str());
  }else
  if( doc_rec["e"][0]["n"]=="screen")
  {
    String val=doc_rec["e"][0]["v"];
    lcd.home();
    lcd.clear();
    if(val.length()>16)
    {
      lcd.print(val.substring(0,16));
      lcd.setCursor(0,1);
      lcd.print(val.substring(16,32));
    }
    else
     lcd.print(val);
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
  counterP=counterP+1;
  counterS=counterS+1;

}
void mooveFan(float step_pos)
{

  int fan_speed=step_pos*255/n_step;
  if(fan_speed>255)
    fan_speed=255;

   
 analogWrite(Fan_Pin,fan_speed);
}

void HeaterOn(float step_pos)
{
  int heat_pow=step_pos*255/n_step;
  if( heat_pow>255)
     heat_pow=255;
  analogWrite(Heat_Pin, heat_pow);
}
/*
void Update()
{
  /* doc_snd.clear();
  doc_snd["ID"]="Yun";
  doc_snd["endPoint"]["light"]=F("tiot/17/home/light");
   doc_snd["endPoint"]["screen"]="tiot/17/home/screen";
   doc_snd["endPoint"]["temperature"]="tiot/17/home/temperature";
   doc_snd["endPoint"]["presence"]="tiot/17/home/presence";
   doc_snd["endPoint"]["noise"]="tiot/17/home/noise";
  doc_snd["avaibleResources"][0]="led";
  doc_snd["avaibleResources"][1]="temperature";
    doc_snd["avaibleResources"][2]="screen";
  doc_snd["avaibleResources"][3]="presence";
  doc_snd["avaibleResources"][4]="noise";
  
  serializeJson(doc_snd,Serial);
 //Serial.println(output);
 
 Serial.println("updated");
String output=Serial.print(output);
 printResponce(postRequest(output));
}*/
void Update(){
  
   Serial.print(heartbit);
  Process p;
  
  p.begin("curl");
  p.addParameter("-H");
  p.addParameter("Content-Type: application/json");
  p.addParameter("-X");
  p.addParameter("POST");
  p.addParameter("-d");
   p.addParameter(heartbit);
  p.addParameter("http://192.168.1.4:8080/device");
  
  p.runAsynchronously();
printResponce( p.exitValue());
}


void printResponce(int code)
{
  Serial.println("Status: "+String(code));

}
String senMlEncode(String res, float v, String unit)
{
  doc_snd.clear();
  doc_snd["bn"]="Yun";
  doc_snd["e"][0]["n"]=res;
   doc_snd["e"][0]["t"]=millis()/1000;
   doc_snd["e"][0]["v"]=v;
  if(unit!="")
    doc_snd["e"][0]["u"]=unit;
  else
     doc_snd["e"][0]["u"]=(char*) NULL; 
  String output;
   
  serializeJson(doc_snd,output);
 delay(1000);
 Serial.println(output);

  return output;
   
}
void loop() {
   mqtt.monitor();
  CheckPresenceP();
  if(counterP<timeout_Pir*60 )// check pir presence
      presenceP=true;
  else
      presenceP=false;
  
     
//this part control if there are people based on the sound sensor
 if(counterS>60 )// check if one minutes is passed
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
  }
  if(presenceS || presenceP)// determinate if there is sameone
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
 if(millis()-tim>10000)
 {   Update(); 
//  Serial.println(millis()-tim);
  
    String message= senMlEncode(("temperature"),ReadTemperature(),"Cel");
   
    
    mqtt.publish(F("tiot/17/house/temperature"),message);
  
    message= senMlEncode("presence",presenceP,"");

    mqtt.publish(F("tiot/17/house/presence"),message);
     Serial.println(message+ "PUBLISH");
    message= senMlEncode("noise",presenceS,"");

    mqtt.publish(F("tiot/17/house/noise"),message);
     Serial.println(message+ "PUBLISH");
    
    tim=millis();
 }
 if(millis()-tim1>60000)
 {
  Update(); 
  tim1=millis();
 }
Serial.println(millis());
}
