import requests 
import json
import threading
import random
import string 
# Making a PUT request
def sendData():
	per_dict = {'fan_speed' : '0', 'heater' : '0'}

	per_dict['fan_speed'] = str(random.randint(0,255))

		
	per_dict['heater'] = str(random.randint(1,60))

	load = json.dumps(per_dict)

	return load
