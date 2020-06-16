import requests 
import json

# Making a PUT request
def getBroker():
      r=requests.get('http://localhost:8080/broker/')
      return r.content
def getDevice(ID):
      if ID == "":
            r=requests.get('http://localhost:8080/device/all')
      else:
            s='http://localhost:8080/device/one?ID='+str(ID)
            r=requests.get(s)
      return r.content
def getUser(ID):
      if ID == "":
            r=requests.get('http://localhost:8080/user/all')
      else:
            s='http://localhost:8080/user/one?ID='+str(ID)
            r=requests.get(s)
      return r.content
if __name__=="__main__":
      print(getBroker())
      print(getDevice(""))
      print(getDevice("Sens1"))
      print(getUser(""))
      print(getUser("mattieri"))
      
   
