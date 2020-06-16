import cherrypy
import json
class TConverter(object):
    exposed=True
    def __init__(self):
        self.namefile="log.json"
        self.first_time=True
        self.counter=0
        pass
   
    def AppendFile(self,data):
        if self.first_time:
            with open(self.namefile, 'w') as file:
                dic={
                    "data":{}
                    }
                dic['data'][self.counter]=(data)
                print(dic)
                json.dump(dic,file)
            self.first_time=False
        else:
            fil=self.LoadFile()
            
            with open(self.namefile, 'w') as file:
                
                fil['data'][self.counter]=(data)
              
                json.dump(fil,file)
        self.counter+=1
    def LoadFile(self):
        with open(self.namefile) as j:
            json_data = json.load(j)
        return json_data
    def converter(self,value,original,target):
            if(original=="C" or original=="c"):
                if(target=="F" or target=="f"):
                    return (value*9/5)+32
                elif (target=="K" or target=="k"):
                    return value+273.15
                elif (target=="C" or target=="c"):
                    return value
                else:
                     raise cherrypy.HTTPError(400,"Bad Request")
            elif(original=="F" or original=="f"):
                if(target=="F" or target=="f"):
                    return value
                elif (target=="K" or target=="k"):
                    return ((value-32)*5/9)+273.15
                elif (target=="C" or target=="c"):
                    return (value-32)*5/9
                else:
                     raise cherrypy.HTTPError(400,"Bad Request")
            elif(original=="K" or original=="k"):
                if(target=="F" or target=="f"):
                    return ((value-273.15)*9/5)+32
                elif (target=="K" or target=="k"):
                    return value
                elif (target=="C" or target=="c"):
                    return value-273
                else:
                     raise cherrypy.HTTPError(400,"Bad Request")
            
    def GET(self,*uri,**params):
        
        error=False
        value=0
        orig=""
        targ=""
        if len(uri)==4:
            if str(uri[0])=="converter":
                value=int(uri[1])
                orig=str(uri[2])
                targ=str(uri[3])
           
            else:
                error=True
        elif str(uri[0])=="log":
                file=self.LoadFile()
                fil=file['data'].values()
                return str(fil)
        else:
            error=True
        with open('data.txt', 'w') as outfile:
            if(error):
                 raise cherrypy.HTTPError(400,"Bad Request")
            else:
                out_dic={
                    "original value":value,
                    "original unit": orig,
                    "converted value":self.converter(value,orig,targ),
                    "target unit":targ
                    }
    def POST(self,*uri,**params):
        if str(uri[0])=="log":
            body=cherrypy.request.body.read()
            json_body=json.loads(body.decode('utf-8'))
           
            self.AppendFile(json_body)
        else:
           raise cherrypy.HTTPError(404,"Not Found") 
    

    
   
            
   
   

if __name__ == '__main__':
    conf={
        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tool.session.on':False
        }
    }
  
    cherrypy.tree.mount(TConverter(),'/',conf)
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.config.update({'server.socket_host':'0.0.0.0'})
    cherrypy.engine.start()
    cherrypy.engine.block()
