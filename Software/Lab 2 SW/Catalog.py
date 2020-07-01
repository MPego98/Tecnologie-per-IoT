import json
import time
import threading
class WorkJson(object):
    def __init__(self,namefile):
        self.namefile=namefile
    def WriteFile(self,data):
        with open(self.namefile, 'w') as file:
            json.dump(data, file)
    def LoadFile(self):
        with open(self.namefile, 'r+') as j:
            json_data = json.load(j)
        return json_data
          
class WorkCatalog(object):
     def __init__(self):
       self.work= WorkJson("Catalog/myCatalog.json")
       
       self.Device_dict={
                "ID":None,
                "endPoint":None,
                "avaibleResources":None,
                "TimeStamp":None
                }
       self.User_dict={
                "ID":None,#email
                "Name":None,
                "Surname":None
                }
       self.Service_dict={
                "ID":None,
                "Description":None,
                "endPoint":None,
                "TimeStamp":None
                }
       self.Catalog={
              "messageBroker":["test.mosquitto.org",1883],
              "Device":{},
              "User":{},
              "Service":{}
              }
       self.work.WriteFile(self.Catalog)
     def addDevice(self,device):
        Cat=self.work.LoadFile()
        updated=False
        if len(Cat['Device'])>0:
            for keys in Cat['Device']:
                if Cat['Device'][keys]['ID']==device['ID']:
                        Cat['Device'][keys]['TimeStamp']=int(time.time())
                        updated=True       
        if(not updated):
            device['TimeStamp']=int(time.time())
            Cat['Device'][len(Cat['Device'])]=device
        self.work.WriteFile(Cat)
            
     def addUser(self,user):
        Cat=self.work.LoadFile()
        updated=False
        if len(Cat['User'])>0:
            for keys in Cat['User']:
                if Cat['User'][keys]['ID']==user['ID']:
                        updated=True       
        if(not updated):
            Cat['User'][len(Cat['User'])]=user
        self.work.WriteFile(Cat)
     def addService(self,service):
        Cat=self.work.LoadFile()
        updated=False
        if len(Cat['Service'])>0:
            for keys in Cat['Service']:
                if Cat['Service'][keys]['ID']==service['ID']:
                        Cat['Service'][keys]['TimeStamp']=int(time.time())
                        updated=True       
        if(not updated):
            service['TimeStamp']=int(time.time())
            Cat['Service'][len(Cat['Service'])]=service
        self.work.WriteFile(Cat) 
     def DeletOld(self):
        attual_time=time.time()
        threading.Timer(60.0, self.DeletOld).start()
        Cat=self.work.LoadFile()
        i=[]
        for keys in Cat['Device']:
            oldTime=int(Cat['Device'][keys]['TimeStamp'])
            if attual_time-oldTime>120:#120 = 2 min
                i.append(keys)
        for ele in i:
            print(Cat['Device'][ele])
            del(Cat['Device'][ele])
        k=[]
        for keys in Cat['Service']:
            oldTime=int(Cat['Service'][keys]['TimeStamp'])
            if attual_time-oldTime>120:#120 = 2 min
               k.append(keys)
        for ele in k:
            del(Cat['Service'][ele])
        self.work.WriteFile(Cat)
     def returnDevice(self,ID):
        Cat=self.work.LoadFile()
        if ID=="":#return all device
            return Cat['Device']
        else:
            for keys in Cat['Device']:
                if Cat['Device'][keys]['ID']== ID:
                    return Cat['Device'][keys]
     def returnUser(self,ID):
        Cat=self.work.LoadFile()
        if ID=="":#return all device
            return Cat['User']
        else:
            for keys in Cat['User']:
                if Cat['User'][keys]['ID']== ID:
                    return Cat['User'][keys]
     def returnService(self,ID):
        Cat=self.work.LoadFile()
        if ID=="":#return all device
            return Cat['Service']
        else:
            for keys in Cat['Service']:
                if Cat['Service'][keys]['ID']== ID:
                    return Cat['Service'][keys]
     def returnBroker(self):
        Cat=self.work.LoadFile()
        return Cat['messageBroker']
        
##if __name__=="__main__":
##    Worker=WorkCatalog()
##  
##    
##    mydev=Worker.Device_dict
##    mydev['ID']=1
##    mydev['endPoint']="boh"
##    mydev['avaibleResources']=("temperature","pir")
##    Worker.add_device(mydev)
##    mydev2=Worker.Device_dict;
##    mydev2['ID']=2
##    mydev2['endPoint']="boh"
##    mydev2['avaibleResources']=("temperature","pir","sound")
##    Worker.add_device(mydev2)
##    tim=time.time()
##    while time.time()-tim<130:
##        print(time.time()-tim)
##        Worker.DeletOld(time.time())
##        myUs1=Worker.User_dict;
##        myUs1['ID']="mattieri"
##        myUs1['Name']="Mattia"
##        myUs1['Surname']="Pego"
##        Worker.add_User(myUs1)
##        mySer1=Worker.Service_dict;
##        mySer1['ID']="cose"
##        mySer1['Description']="FaccioCose"
##        mySer1['endPoint']="boh"
##        Worker.add_Service(mySer1)
##    
##    
##    print("done")
    
