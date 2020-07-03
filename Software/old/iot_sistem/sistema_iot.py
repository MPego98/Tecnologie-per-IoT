import requests 
import json
import threading
import random
import string
import time
from Subscriber import Subscriber
from Publisher import Publisher
class iot_device(object):
        def __init__(self,name):
           self.name=name
           self.broker=[]
           self.Publish=None
        def MessageReceived(self, paho_mqtt , userdata, msg):
                    # A new message is received
                    
                    body=msg.payload.decode("utf-8")

                    json_body = json.loads(body)
                    #nelle righe successive ci sarebbe il controllo delle uscite
                    #che vanno al condizionamento e al riscaldamento
                    print("FAN :" + str(json_body['Fan']))
                    print("Heater :" + str(json_body['Heat']))

        def sendData(self):
                threading.Timer(2.0, self.sendData).start()
                per_dict = {'temperature' : 0, 'unit' : 'C', 'presence' : False}

                per_dict['temperature'] = str(random.randint(1,60))

                        
                per_dict['presence'] = str(random.choice([True, False]))

                load = json.dumps(per_dict)
               
                self.Publish.myPublish("/tiot/17/house/sens",load)
               
                
        def alive(self):         
            threading.Timer(60.0, self.alive).start()
            load=json.dumps({
                      "ID": self.name,
                  "endPoint": "/tiot/17/house/sens",
                  "avaibleResources": ["Temperature", "sound"]
                })
            requests.put('http://localhost:8080/device/', data=load)  
        def set(self):
             print("ok?")
             self.Publish=Publisher("pub",self.broker)
             self.Publish.start()
if __name__=="__main__":
    mydevice=iot_device("house")
    mydevice.alive()
    broker=requests.get('http://localhost:8080/broker/')
    
    mydevice.broker=broker.json()
  
    mydevice.set()
    s='http://localhost:8080/service/one?ID=Smart_House'
    go=True
    TempSub=None
    while go:
        print(go)
        try:
            topic=requests.get(s)
            topic=topic.json()
           
            
            go=False
        except:
            go=True
    #TempSub=Subscriber("Temperature",mydevice.broker,topic['endPoint'],mydevice.MessageReceived )
   # TempSub.start()
    mydevice.sendData()
    a = 0
    while (a < 100):
            a += 1
            time.sleep(2)

    #TempSub.stop()
        
        
