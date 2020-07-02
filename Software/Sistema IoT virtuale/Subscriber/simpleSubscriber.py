import paho.mqtt.client as PahoMQTT
import time
import json



#from Catalog import WorkCatalog
#worker=WorkCatalog()
class MySubscriber:
		def __init__(self, clientID):
			self.clientID = clientID
			# create an instance of paho.mqtt.client
			self._paho_mqtt = PahoMQTT.Client(clientID, False) 

			# register the callback
			self._paho_mqtt.on_connect = self.myOnConnect
			self._paho_mqtt.on_message = self.myOnMessageReceived

			self.topic = '/deviceMQTT'
			#self.messageBroker = 'mqtt.eclipse.org'
			self.messageBroker = 'localhost'


		def start (self):
			#manage connection to broker
			self._paho_mqtt.connect(self.messageBroker, 1883)
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
			#json_body=body
			
			#device=worker.Device_dict

			print (str(body))
			#device['ID']=json_body['ID']

			

			#device['endPoint']=json_body['endPoint']
			#device['avaibleResources']=json_body['avaibleResources']
			#print(device)

			
			#worker.addDevice(device)

			

if __name__ == "__main__":
	test = MySubscriber("MySubscriber 1")
	test.start()

	a = 0
	while (a < 30):
		a += 1
		time.sleep(1)

	test.stop()
