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
            
    def GET(self,*uri,**params):
        error=False
        value=0
        orig=""
        targ=""
        if len(uri)!=0:
            if str(uri[0])=="converter":
             for par in params.keys():
                if(par=="value"):
                    if str(params["value"]).isnumeric():
                        value=int(params["value"])
                    else:
                        error=True
                elif(par=="originalUnit"):
                    if str(params["originalUnit"])!="":
                        orig=str(params["originalUnit"])
                    else:
                        error=True
                elif(par=="targetUnit"):
                    if str(params["targetUnit"])!="":
                        targ=str(params["targetUnit"])
                    else:
                        error=True
                else:
                    error=True
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
                return json.dump(out_dic,outfile)

if __name__ == '__main__':
    conf={
        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tool.session.on':True
        }
    }       
    cherrypy.tree.mount(TConverter(),'/',conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
