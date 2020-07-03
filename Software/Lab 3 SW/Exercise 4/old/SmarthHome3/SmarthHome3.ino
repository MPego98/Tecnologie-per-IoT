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
//heater
float The_min_abs=15.0,The_min_pres=14.0,The_max_abs=17.0,The_max_pres=28.0,The_Max,The_Min;
//sound
volatile int counterS=0;
//expressed in minutes
volatile bool presenceS=false;
volatile int counter_event=0;
//int MobileBlock[event_time];
int abs_time=0; //rapresente the number of time that for "time_event" minute the is not enought sound
volatile  int wait=0;
//pir
volatile  int counterP=0;
volatile bool presenceP=false;
volatile int counter_eventP=0;

String heartbit;
const int capacity= JSON_OBJECT_SIZE(2)+JSON_ARRAY_SIZE(1)+JSON_OBJECT_SIZE(5)+40;
DynamicJsonDocument doc_snd(capacity);
//DynamicJsonDocument doc_rec(capacity);
void setup() {
  
  Serial.begin(9600);
  //while(!Serial);
  Serial.println("starting...");
 pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN,HIGH);
   //Timer1.initialize(1 *1e6);
  //Timer1.attachInterrupt(Update_Stat);
  //lcd set
  /*lcd.begin(16,2);
  lcd.setBacklight(150);
  lcd.home();
  lcd.clear();*/
  /*pinMode(Led_Pin, OUTPUT);
  //fan set
  pinMode(Fan_Pin,OUTPUT);
 //analogWrite(Fan_Pin,0);
  //heater set
  pinMode(Heat_Pin,OUTPUT);
 //analogWrite(Heat_Pin,0);
  //temperature set
  pinMode(Temp_Pin,INPUT);
  //sound set
  pinMode(Sound_Pin,INPUT);
// attachInterrupt(digitalPinToInterrupt(Sound_Pin),CheckPresenceS,RISING);
  //Pir set
  pinMode(Pir_Pin,INPUT);*/

  mqtt.begin("test.mosquitto.org",1883);
  mqtt.subscribe("tiot/17/home/light",setLedValue);
 // mqtt.subscribe("tiot/17/home/screen",setScreenValue);
  //Writing Temperature Parameter
  //StartParameter();
  Tac_Max=Tac_max_abs;
  Tac_Min=Tac_min_abs;
  The_Max=The_max_abs;
  The_Min=The_min_abs;
  Serial.println("started");
 
}
float ReadTemperature()
{
  int a = analogRead(Temp_Pin);

    float R = 1023.0/a-1.0;
    R = R0*R;
   float temperature = (1.0/((log(R/R0)/B)+(1/298.15)))-273.15; // convert to temperature via datasheet
 return temperature;
}
void Update_Stat()
{
   doc_snd.clear();
  doc_snd["bn"]="Yun";
  doc_snd["e"][0]["n"]="Temperature";
   doc_snd["e"][0]["t"]=millis()/1000;
   doc_snd["e"][0]["v"]=ReadTemperature();
    doc_snd["e"][0]["u"]="C";

  String output;
  serializeJson(doc_snd,output);
Serial.println(output);
 printResponce(postRequest(output));
}
void setLedValue(const String& topic, const String& subtopic, const String& message)
{
  DeserializationError err = deserializeJson(doc_snd,message);
  if(err)
  {
    Serial.print(F("deserializedJson failed with code"));
    Serial.println(err.c_str());
  }else
  if( doc_snd["e"][0]["n"]=="led")
  {
    int val=doc_snd["e"][0]["v"];
    if(val==1||val==0)
    {
      digitalWrite(Led_Pin,val);
    }
  }
}
int postRequest(String data){
  Process p;
  
  p.begin("curl");
  p.addParameter("-H");
  p.addParameter("Content-Type: application/json");
  p.addParameter("-X");
  p.addParameter("PUT");
  p.addParameter("-d");
  p.addParameter(data);
 //  p.addParameter(F("{\"ID\":\"Yun\",\"endPoint\":\"tiot/17/home\",\"avaibleResources\":[\"led\",\"temperature\",\"screen\",\"presence\",\"noise\"]}"));

  p.addParameter("http://192.168.1.4:8080/device");
  
  p.run();

  return p.exitValue();
}
void printResponce(int code)
{
  Serial.println("Status: "+String(code));

}
void loop() {
 
if(millis()-tim>5000)
  {
  
    Update_Stat();
    tim=millis();
    
  }

 

}
