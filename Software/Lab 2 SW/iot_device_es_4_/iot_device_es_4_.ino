#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <Process.h>
#include <ArduinoJson.h>


#define B 4275
#define  R0 100000

//temperature sensor
const int Temp_Pin= A1;
long int tim=0;
const int capacity= JSON_OBJECT_SIZE(2)+JSON_ARRAY_SIZE(1)+JSON_OBJECT_SIZE(5)+40;
DynamicJsonDocument doc_snd(capacity);
void setup() {
  
  pinMode(Temp_Pin,INPUT);
 
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
  Bridge.begin();
  digitalWrite(LED_BUILTIN,HIGH);
  Serial.begin(9600);
  Serial.println("starting...");


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
  doc_snd["ID"]="Yun";
  doc_snd["endPoint"]="boh";
   doc_snd["avaibleResources"]="temperature";

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
 
if(millis()-tim>30000)
  {
   // Serial.println("30 sec");
    Update_Stat();
    tim=millis();
    
  }

 

}
