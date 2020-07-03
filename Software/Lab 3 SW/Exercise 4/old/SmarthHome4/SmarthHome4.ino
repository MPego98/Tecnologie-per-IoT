#include <MQTTclient.h>

#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <Process.h>
#include <ArduinoJson.h>


#define B 4275
#define  R0 100000

//temperature sensor
const int Temp_Pin= A1;
const int Led_Pin= 7;
long int tim=0;
const int capacity= JSON_OBJECT_SIZE(2)+JSON_ARRAY_SIZE(1)+JSON_OBJECT_SIZE(5)+40;
DynamicJsonDocument doc_snd(capacity);
DynamicJsonDocument doc_rec(capacity);
void setup() {
  Serial.begin(9600);
  Serial.println("starting...");
  pinMode(Temp_Pin,INPUT);
 pinMode(Led_Pin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN,HIGH);
  mqtt.begin("test.mosquitto.org",1883);
  mqtt.subscribe("tiot/17/house/control",setLedValue);


}
void setLedValue(const String& topic, const String& subtopic, const String& message)
{
  DeserializationError err = deserializeJson(doc_rec,message);
    Serial.print(message);
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
float ReadTemperature()
{
  int a = analogRead(Temp_Pin);

    float R = 1023.0/a-1.0;
    R = R0*R;
   float temperature = (1.0/((log(R/R0)/B)+(1/298.15)))-273.15; // convert to temperature via datasheet
 return temperature;
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
 
  return output;
   
}

void loop() {
 
  mqtt.monitor();
  if(millis()-tim>300)
  {
    String message= senMlEncode("temperature",ReadTemperature(),"Cel");
    Serial.println(message);
    mqtt.publish("tiot/17/temperature",message);
    delay(1000); 
    tim=millis();
  }
}
