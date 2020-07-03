import time
import json
import requests
import threading
from Subscriber import Subscriber
from Publisher import Publisher

dic={
            "water":False,
            "light":False,
            "Heat":0
        }
def sendData():         
    threading.Timer(60.0, sendData).start()
    load=json.dumps({
              "ID": "Serra",
              "Description":"Control the smart house",
              "endPoint":"/tiot/17/serra/control"
            })
    requests.put('http://localhost:8080/service/', data=load)        
def ReceivedData(paho_mqtt , userdata, msg):
    body=msg.payload.decode("utf-8")                
    json_body = json.loads(body)
    
    dic['water'],dic['light'],dic['Heat']= compute(json_body['temperature'],json_body['light perc'],json_body['umidity'])
    
def compute(T,L,U):
    temp=255-((8/255)*(T-4))#calcola il valore tra 0 e 255 del riscaldamento
    if temp>255:
        temp=255
    elif temp<0:
        temp=0
    if L<25:#se la percentuale di luce è sotto il 25% accendo le luci
        light=True
    else:
        light=False
    if U<40:#se umidità nel terreno è minore del 40% accendo la pompa dell'acqua
        pump=True
    elif U>85:# se umidità maggiore dell'85% spengo la pompa
        pump=False
    return pump,light,temp

if __name__ == "__main__":
    sendData()
    broker=requests.get('http://localhost:8080/broker/')
    broker=broker.json()
    s='http://localhost:8080/device/one?ID=serra'
    topic=requests.get(s)
    topic=topic.json()
    sensorSub=Subscriber("sensor",broker,topic['endPoint'], ReceivedData)
    
    Publish = Publisher("pub",broker)
    sensorSub.start()

    Publish.start()
    a = 0
 
    while (a < 100):
        a += 1
        print(dic)
        Publish.myPublish("/tiot/17/serra/control",json.dumps(dic))
        time.sleep(10)
    sensorSub.stop()
    
    Publish.stop()

