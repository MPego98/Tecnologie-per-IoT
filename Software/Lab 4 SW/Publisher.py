import paho.mqtt.client as PahoMQTT
import time
import json





class Publisher:
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
                pass
                #print ("Connected Publisher to %s with result code: %d" % (self.messageBroker, rc))

