#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <ArduinoJson.h>
#define B 4275
#define  R0 100000
BridgeServer server;
const int Light_Pin =6;
//temperature sensor
const int Temp_Pin= A1;

const int capacity= JSON_OBJECT_SIZE(2)+JSON_ARRAY_SIZE(1)+JSON_OBJECT_SIZE(5)+40;
DynamicJsonDocument doc_snd(capacity);
void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.print(1);
  pinMode(Light_Pin,OUTPUT);
  digitalWrite(Light_Pin,LOW);
  pinMode(Temp_Pin,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN,HIGH);
  server.listenOnLocalhost();
  server.begin();

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
float ReadTemperature()
{
  int a = analogRead(Temp_Pin);

    float R = 1023.0/a-1.0;
    R = R0*R;
   float temperature = (1.0/((log(R/R0)/B)+(1/298.15)))-273.15; // convert to temperature via datasheet
 return temperature;
}
void process(BridgeClient client)
{
  String command=client.readStringUntil('/');
  command.trim();
  Serial.println(command);
  if(command=="led")
  {
    
    int val=client.parseInt();
    if(val==1||val==0)
    {
      digitalWrite(Light_Pin,val);
      printResponce(client,200,senMlEncode(F("led"),val,F("")));
    }
    else
      printResponce(client,400,"");
  }
  else if(command=="temperature")
  {
    printResponce(client,200,senMlEncode(F("temperature"),ReadTemperature(),F("Cel")));
  }
  else
     printResponce(client,404,"");
}
void printResponce(BridgeClient client,int code,String body)
{
  client.println("Status: "+String(code));
  if(code==200)
  {
    client.println(F("Content-type: application/json; charset=utf-8"));
    client.println();
    client.println(body);
  }
}
void loop() {
 BridgeClient client=server.accept();

 if(client)
 {

  process(client);
  client.stop();
 }
 delay(50);

}
