import cherrypy
import json

from Catalog import WorkCatalog
worker=WorkCatalog()
class Device(object):
     
      exposed=True
      def __init__(self):
            pass
      def PUT(self, **params):
            body=cherrypy.request.body.read()
            print(str(body))
            json_body=json.loads(body.decode('utf-8'))
            device=worker.Device_dict
            device['ID']=json_body['ID']
            device['endPoint']=json_body['endPoint']
            device['avaibleResources']=json_body['avaibleResources']
            print(device)
            worker.addDevice(device)
            
      def GET(self,*uri,**params):
        #Standard output
        if len(uri)!=0:
            if str(uri[0])=="all":
                return json.dumps(worker.returnDevice(""))
            elif str(uri[0])=="one":
                if params!={}:
                 print(params.keys())
                 if "ID" in params:
                     if params['ID']!= "":
                        return json.dumps( worker.returnDevice(params['ID']))
                     else:
                        raise cherrypy.HTTPError(400)
                 else :
                     cherrypy.HTTPError(400)
            else:
             raise cherrypy.HTTPError(400)
        else:
            raise cherrypy.HTTPError(400)

class Service(object):
    
      exposed=True
      def __init__(self):
            pass
      def PUT(self, **params):
            body=cherrypy.request.body.read()
            json_body=json.loads(body.decode('utf-8'))
            service=worker.Service_dict
            service['ID']=json_body['ID']
            service['endPoint']=json_body['endPoint']
            service['Description']=json_body['Description']
            worker.addService(service)
          
      def GET(self,*uri,**params):
        #Standard output
        if len(uri)!=0:
            if str(uri[0])=="all":
                return json.dumps(worker.returnService(""))
            elif str(uri[0])=="one":
                if params!={}:
                    if "ID" in params:
                         if params['ID']!= "":
                            return json.dumps(worker.returnService(params['ID']))
                         else:
                            raise cherrypy.HTTPError(403)
                    else:
                         raise cherrypy.HTTPError(400)
            else:
             raise cherrypy.HTTPError(400)
        else:
            raise cherrypy.HTTPError(400)
class User(object):
     
      exposed=True
      def __init__(self):
            pass
      def PUT(self, **params):
            body=cherrypy.request.body.read()
            json_body=json.loads(body.decode('utf-8'))
            service=worker.User_dict
            service['ID']=json_body['ID']
            service['Name']=json_body['Name']
            service['Surname']=json_body['Surname']
            worker.addUser(service)
          
      def GET(self,*uri,**params):
        #Standard output
        if len(uri)!=0:
            if str(uri[0])=="all":
                return json.dumps(worker.returnUser(""))
            elif str(uri[0])=="one":
                if params!={}:
                 if params['ID']!= "":
                      if "ID" in params:
                            return json.dumps(worker.returnUser(params['ID']))
                      else:
                            raise cherrypy.HTTPError(400)
                 else:
                     raise cherrypy.HTTPError(400)
            else:
             raise cherrypy.HTTPError(400)
        else:
            raise cherrypy.HTTPError(400)
class Broker(object):
     
      exposed=True
      def __init__(self):
            pass
          
      def GET(self,*uri,**params):
         return json.dumps(worker.returnBroker())
                   



if __name__ == '__main__':
      conf={
            '/':{
                        'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                        'tool.session.on':True
                        
            }
      }
      cherrypy.config.update({'server.socket_port': 8080})
      cherrypy.tree.mount(Device(),'/device/',conf)
      cherrypy.tree.mount(Service(),'/service/',conf)
      cherrypy.tree.mount(User(),'/user/',conf)
      cherrypy.tree.mount(Broker(),'/broker/',conf)
      cherrypy.config.update({'server.socket_host':'0.0.0.0'})
      worker.DeletOld()
      cherrypy.engine.start()
      cherrypy.engine.block()

    
