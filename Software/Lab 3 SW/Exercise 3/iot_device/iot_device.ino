#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <Process.h>
#include <ArduinoJson.h>
#include <MQTTclient.h>

#define B 4275
#define  R0 100000

//temperature sensor
const int Led_Pin= 7;
long int tim=0;
const int capacity= JSON_OBJECT_SIZE(2)+JSON_ARRAY_SIZE(1)+JSON_OBJECT_SIZE(5)+40;
DynamicJsonDocument doc_rec(capacity);
DynamicJsonDocument doc_snd(capacity);
void setup() {
  
 pinMode(Led_Pin, OUTPUT);
 
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN,HIGH);
  Serial.begin(9600);
  Serial.println("starting...");
  mqtt.begin("test.mosquitto.org",1883);
  mqtt.subscribe("tiot/17/led",setLedValue);
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
void Update_Stat()
{
   doc_snd.clear();
  doc_snd["ID"]="Yun";
  doc_snd["endPoint"]="tiot/17/led";
  doc_snd["avaibleResources"]="led";
  String output;
  serializeJson(doc_snd,output);
 Serial.println(output);
 printResponce(postRequest(output));
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

  p.addParameter("http://192.168.1.8:8080/device");
  
  p.run();

  return p.exitValue();
}


void printResponce(int code)
{
  Serial.println("Status: "+String(code));

}
void loop() {
 mqtt.monitor();
if(millis()-tim>30000)
  {
   // Serial.println("30 sec");
    Update_Stat();
    
    tim=millis();
    
  }

 

}
