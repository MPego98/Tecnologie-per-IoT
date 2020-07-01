import cherrypy
import json
class TConverter(object):
    exposed=True
    def __init__(self):
        pass
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
            
   
    def PUT(self,**params):
        body=cherrypy.request.body.read()
        json_body=json.loads(body.decode('utf-8'))
        dic={"values":None,
             "originalUnit":None,
             "targetUnit": None,
             "converted":[]}
        for v in json_body['values']:
            dic['converted'].append(self.converter(v,json_body['originalUnit'],json_body['targetUnit']) )   
        dic['values']=json_body['values']
        dic['originalUnit']=json_body['originalUnit']
        dic['targetUnit']=json_body['targetUnit']
        return json.dumps(dic)
if __name__ == '__main__':
    conf={
        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tool.session.on':False
        }
    }       
    cherrypy.tree.mount(TConverter(),'/',conf)
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
