import paho.mqtt.client as PahoMQTT
import time
import json

from Iot_Device_mqtt import sendData



class MyPublisher:
	def __init__(self, clientID):
		self.clientID = clientID

		# create an instance of paho.mqtt.client
		self._paho_mqtt = PahoMQTT.Client(self.clientID, False) 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect

		#self.messageBroker = 'mqtt.eclipse.org'
		self.messageBroker = 'localhost'

	def start (self):
		#manage connection to broker
		self._paho_mqtt.connect(self.messageBroker, 1883)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myPublish(self, topic, message):
		# publish a message with a certain topic
		self._paho_mqtt.publish(topic, message, 2)

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))



if __name__ == "__main__":
	test = MyPublisher("MyPublisher")
	test.start()

	#aspetto 3 secondi prima di inviare il secondo messaggio 
	#quando il contatore a e' arrivato a 20 chiudo il publish

	a = 0
	while (a < 20):
		message = sendData()

		test.myPublish ('/deviceMQTT', message) 	
		a += 1
		time.sleep(3)

	test.stop()


