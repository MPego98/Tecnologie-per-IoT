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



//temperature sensor



//heater



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

 const int capacity= JSON_OBJECT_SIZE(3)+JSON_ARRAY_SIZE(5)+JSON_OBJECT_SIZE(5)+40;
  DynamicJsonDocument doc_rec(capacity);
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
 //analogWrite(Fan_Pin,0);
  //heater set
  pinMode(Heat_Pin,OUTPUT);
 //analogWrite(Heat_Pin,0);
  //temperature set
  pinMode(Temp_Pin,INPUT);
  //sound set
  pinMode(Sound_Pin,INPUT);
  attachInterrupt(digitalPinToInterrupt(Sound_Pin),CheckPresenceS,RISING);
  //Pir set
  pinMode(Pir_Pin,INPUT);
  //Serial set

  mqtt.begin("test.mosquitto.org",1883);
  mqtt.subscribe("tiot/17/house/control/#",setValue);


  

  
}


void setValue(const String& topic, const String& subtopic, const String& message)
{
  DeserializationError err = deserializeJson(doc_rec,message);
  if(err)
  {
    Serial.print(F("deserializedJson failed with code"));
    Serial.println(err.c_str());
  }else
  {
  if( doc_rec["e"][0]["n"]=="led")
  {
    int val=doc_rec["e"][0]["v"];
    if(val==1||val==0)
    {
      digitalWrite(Led_Pin,val);
    }
  }
  else  if( doc_rec["e"][0]["n"]=="Heat")
  {
    int val=doc_rec["e"][0]["v"];
    HeaterOn(val);
  }
   else  if( doc_rec["e"][0]["n"]=="Fan")
  {
    int val=doc_rec["e"][0]["v"];
    mooveFan(val);
  }
  else  if( doc_rec["e"][0]["n"]=="screen")
  {
    String val=doc_rec["e"][0]["v"];
    setScreenValue(val);
  }
}
}
void setScreenValue( String val)
{
 
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
void mooveFan(int fan_speed)
{
 analogWrite(Fan_Pin,fan_speed);
}

void HeaterOn(int heat_pow)
{
  analogWrite(Heat_Pin, heat_pow);
}

void Update(){
 
  Process p;
  p.begin("curl");
  p.addParameter("-H");
  p.addParameter("Content-Type: application/json");
  p.addParameter("-X");
   
  p.addParameter("PUT");
  p.addParameter("-d");
  p.addParameter(F("{\"ID\":\"Yun\",\"endPoint\":\"/tiot/17/home/sens\",\"avaibleResources\":[\"led\",\"temperature\",\"screen\",\"presence\",\"noise\"]}"));

  p.addParameter("http://192.168.1.7:8080/device");
  
  p.run();
  printResponce(p.exitValue());
}


void printResponce(int code)
{
  Serial.println("Status: "+String(code));

}
String senMlEncode(String res, float v, String unit)
{
   String unita;
  if(unit!="")
    unita=unit;
  else
    unita=(char*) NULL; 
  String output="{\"bn\":\"Yun\",\"e\":{\"n\":"+res+",\"t\":"+String(millis()/1000)+",\"v\":"+String(v)+",\"u\":"+unita+"}}";
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
 

  //Serial.println(temp);
 if(millis()-tim>10000)
 { 
    String message= senMlEncode(("temperature"),ReadTemperature(),"Cel");
    mqtt.publish(F("tiot/17/house/sens/temperature"),message);
    message= senMlEncode("presence",presenceP,"");
    mqtt.publish(F("tiot/17/house/sens/presence"),message);
    message= senMlEncode("noise",presenceS,"");
    mqtt.publish(F("tiot/17/house/sens/noise"),message);
 
    tim=millis();
 }
 if(millis()-tim1>60000)
 {
  Update(); 
  tim1=millis();
 }
}
