import requests 
import json
import threading
import random
import string 
# Making a PUT request
def sendData():
	per_dict = {'temperature' : '0', 'unit' : 'C', 'presence' : 'False'}

	per_dict['temperature'] = str(random.randint(1,60))

		
	per_dict['presence'] = str(random.choice([True, False]))

	load = json.dumps(per_dict)

	return load
