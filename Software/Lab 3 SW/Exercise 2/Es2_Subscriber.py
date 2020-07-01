import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import threading
class MySubscriber:
        def __init__(self, clientID,broker,topic):
            self.clientID = clientID
            # create an instance of paho.mqtt.client
            self._paho_mqtt = PahoMQTT.Client(clientID, False) 

            # register the callback
            self._paho_mqtt.on_connect = self.myOnConnect
            self._paho_mqtt.on_message = self.myOnMessageReceived

            self.topic = topic
            #self.messageBroker = 'mqtt.eclipse.org'
            self.messageBroker = broker[0]
            self.port=broker[1]



        def start (self):
            #manage connection to broker
            self._paho_mqtt.connect(self.messageBroker, self.port)
            self._paho_mqtt.loop_start()
            # subscribe for a topic
            self._paho_mqtt.subscribe(self.topic, 2)

        def stop (self):
            self._paho_mqtt.unsubscribe(self.topic)
            self._paho_mqtt.loop_stop()
            self._paho_mqtt.disconnect()

        def myOnConnect (self, paho_mqtt, userdata, flags, rc):
            print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

        def myOnMessageReceived (self, paho_mqtt , userdata, msg):
            # A new message is received
            
            body=msg.payload.decode("utf-8")
            #print ("Message Recived: " + str(body) )

            json_body = json.loads(body)
            print(str(json_body['e'][0]['v'])+" "+str(json_body['e'][0]['u']))

def sendData():         
    threading.Timer(60.0, sendData).start()
    load=json.dumps({
              "ID": "Yun Temperature",
              "Description":"Get T from yun publisher",
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
    test = MySubscriber("MySubscriber 1",broker,topic['endPoint'])
    test.start()

    a = 0
    while (a < 100):
        a += 1
        time.sleep(1)

    test.stop()
