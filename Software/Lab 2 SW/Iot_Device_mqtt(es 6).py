import requests 
import json
import threading
import random
import string 
# Making a PUT request
def sendData():
      per_dict = {'ID' : '15', 'endPoint' : 'K', 'avaibleResources' : 'C'}

      per_dict['ID'] = str(random.randint(1,101))

      rand_endpoint = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = random.randint(1,10))) 

      per_dict['endPoint'] = str(rand_endpoint)

      rand_avaibleResources = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = random.randint(1,10)))

      per_dict['avaibleResources'] = str(rand_avaibleResources)
      #dct = random.choice(list(per_dict.items()))

      load = json.dumps(per_dict)

      return load
