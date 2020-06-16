import requests 
import json
import threading
# Making a PUT request
def sendData():
      threading.Timer(60.0, sendData).start()
      load=json.dumps({
              "ID": "Sens1",
              "endPoint": "Don't know what is",
              "avaibleResources": ["Temperature", "sound"]
            })
      requests.put('http://localhost:8080/device', data=load)
      load=json.dumps({
              "ID": "Sens2",
              "endPoint": "Don't know what is",
              "avaibleResources": ["Temperature", "pir"]
            })
      requests.put('http://localhost:8080/device', data=load)
if __name__=="__main__":
      sendData()
   
