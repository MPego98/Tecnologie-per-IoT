import time
import json
import requests
import threading
from Subscriber import Subscriber
from Publisher import Publisher
temperature=0
noise=False
presence=False
TPFM=30 #Temperature Presence Fan Max
TPFm=20 #Temperature Presence Fan Min
TPHM=15 #Temperature Presence Heater Max
TPHm=10 #Temperature Presence Heater Min
TAFM=30 #Temperature Absence Fan Max
TAFm=20 #Temperature Absence Fan Min
TAHM=15 #Temperature Absence Heater Max
TAHm=10 #Temperature Absence Heater Min
TFM=0
TFm=0
THM=0
THm=0
def sendData():         
    threading.Timer(60.0, sendData).start()
    load=json.dumps({
              "ID": "Smart House",
              "Description":"Control the smart house",
              "endPoint":"",
            })
    requests.put('http://localhost:8080/service/', data=load)        
           
def GetData(self, paho_mqtt , userdata, msg):
            # A new message is received
            body=msg.payload.decode("utf-8")
            json_body = json.loads(body)
            if doc_rec["e"][0]["n"]=="temperature":
                temperature=doc_rec["e"][0]["v"]
            elif doc_rec["e"][0]["n"]=="presence":
                presence=doc_rec["e"][0]["v"]
            elif doc_rec["e"][0]["n"]=="noise":
                noise=doc_rec["e"][0]["v"]
        
        
def control():
    if presence or noise :#controlla se è presente qualcuno a seconda del rumore o del sensore pir
        TFM=TPFM
        TFm=TPFm
        THM=TPHM
        THm=THm
    else:
        TFM=TAFM
        TFm=TAFm
        THM=TAHM
        THm=TAm
    fan=(temperature-TFm)*((TFM-TFm)/255)
    heat=(THM-temperature)*((THM-THm)/255)
    return fan,heat
if __name__ == "__main__":
    sendData()
    broker=requests.get('http://localhost:8080/broker/')
    broker=broker.json()
    s='http://localhost:8081/device/one?ID=Yun'
    topic=requests.get(s)
    topic=topic.json()
    Sub=Subscriber("Temperature",broker,topic['endPoint'],GetData)
    Publish = Publisher("pub",broker)
    Sub.start()
    Publish.start()
    a = 0
    on=false
    while True:
        a += 1
        if on:
                l=1
        else:
                l=0
        light ={
                  "bn":"control",
                  "e":[
                          {
                           "n":"led",
                           "t":time.time(),
                           "v":l,
                           "u":None
                           }
                     ]
                }
        
        Publish.myPublish("/tiot/17/home/control/light",json.dumps(light))
        if on:
                t="acceso"
        else:
                t="spento"
        text ={
                  "bn":"Control",
                  "e":[
                          {
                           "n":"screen",
                           "t":time.time(),
                           "v":t,
                           "u":None
                           }
                     ]
                }
        Publish.myPublish("/tiot/17/home/control/screen",json.dumps(text))
        fan,heat=control();
        fan_j ={
                  "bn":"control",
                  "e":[
                          {
                           "n":"Fan",
                           "t":time.time(),
                           "v":fan,
                           "u":None
                           }
                     ]
                }
        heat_j ={
                  "bn":"control",
                  "e":[
                          {
                           "n":"Heat",
                           "t":time.time(),
                           "v":heat,
                           "u":None
                           }
                     ]
                }
        Publish.myPublish("/tiot/17/home/control/fan",json.dumps(fan_j))
        Publish.myPublish("/tiot/17/home/control/heat",json.dumps(heat_j))
        on=not on
        time.sleep(10)
    Sub.stop()
    Publish.stop()

