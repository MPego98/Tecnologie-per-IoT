import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import threading




class MyPublisher:
        def __init__(self, clientID,broker):
                self.clientID = clientID

                # create an instance of paho.mqtt.client
                self._paho_mqtt = PahoMQTT.Client(self.clientID, False) 
                # register the callback
                self._paho_mqtt.on_connect = self.myOnConnect
            #self.messageBroker = 'mqtt.eclipse.org'
                self.messageBroker = broker[0]
                self.port=broker[1]

        def start (self):
                #manage connection to broker
                self._paho_mqtt.connect(self.messageBroker, self.port)
                self._paho_mqtt.loop_start()

        def stop (self):
                self._paho_mqtt.loop_stop()
                self._paho_mqtt.disconnect()

        def myPublish(self, topic, message):
                # publish a message with a certain topic
                self._paho_mqtt.publish(topic, message, 2)

        def myOnConnect (self, paho_mqtt, userdata, flags, rc):
                print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

def sendData():         
    threading.Timer(60.0, sendData).start()
    load=json.dumps({
              "ID": "Yun Light",
              "Description":"Set light of yun ",
              "endPoint":"",
            })
    requests.put('http://localhost:8080/service/', data=load)    

if __name__ == "__main__":
        sendData()
        broker=requests.get('http://localhost:8080/broker/')
        broker=broker.json()
        s='http://localhost:8080/device/one?ID=Yun'
        topic=requests.get(s)
        topic=topic.json()
        test = MyPublisher("MyPublisher",broker)
        test.start()


        a = 0
        
        while (a < 20):
                message ={
                  "bn":"Yun Light",
                  "e":[
                          {
                           "n":"led",
                           "t":"",
                           "v":0,
                           "u":None
                           }
                     ]
                }
                        

                test.myPublish (topic['endPoint'],json.dumps(message))
                print(message)
                a += 1
                time.sleep(3)

        test.stop()


