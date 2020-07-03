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
                    print(body)    
                    json_body = json.loads(body)
                    #nelle righe successive ci sarebbe il controllo delle uscite
                    #che vanno al condizionamento e al riscaldamento
                    print("Activate water pump:" + str(json_body['water']))
                    print("Light on:" + str(json_body['light']))
                    print("heather: " +  str(int(json_body['Heat'])))

        def sendData(self):
                per_dict = {'temperature' : 0, 'unit' : 'C', 'light perc' : None,"umidity":None}

                per_dict['temperature'] = (random.randint(10,40))

                        
                per_dict['light perc'] = (random.randint(0,100))#% di luce nella serra
                
                per_dict['umidity'] = (random.randint(0,100))#% di umidità nel terreno
                load = json.dumps(per_dict)
               
                self.Publish.myPublish("/tiot/17/serra/sens",load)
               
                
        def alive(self):         
            threading.Timer(60.0, self.alive).start()
            load=json.dumps({
                  "ID": self.name,
                  "endPoint": "/tiot/17/serra/sens",
                  "avaibleResources": ["Temperature", "umidity","light level"]
                })
            requests.put('http://localhost:8080/device/', data=load)  
        def set(self):
             self.Publish=Publisher("pub",self.broker)
             self.Publish.start()
if __name__=="__main__":
    mydevice=iot_device("serra")
    mydevice.alive()
    broker=requests.get('http://localhost:8080/broker/')
    
    mydevice.broker=broker.json()
  
    mydevice.set()
    s='http://localhost:8080/service/one?ID=Serra'
    go=True
    TempSub=None
    while go:
        try:
            topic=requests.get(s)
            topic=topic.json()
           
            if topic!= None:
               go=False
        except:
            go=True
    print(topic['endPoint'])
    Sub=Subscriber("Actuator",mydevice.broker,topic['endPoint'],mydevice.MessageReceived )
    Sub.start()
    mydevice.sendData()
    a = 0
    while (a < 100):
            mydevice.sendData()
            a += 1
            time.sleep(2)

    Sub.stop()
        
        
