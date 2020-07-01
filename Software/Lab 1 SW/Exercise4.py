
import cherrypy
import os
import json

PATH = os.getcwd()
HOST = "0.0.0.0"


class WebApp():

    exposed = True
    def GET(self, *uri, **params):
        return open("freeboard/index.html","r")

    def POST(self, *uri, **params):
        if uri[0] == "saveDashboard":
            path = "dashboard/"
            with open("freeboard/dashboard/dashboard.json", "w") as file:
                file.write(params['json_string'])

if __name__ == "__main__":
    conf={
	
	"/":{
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'tools.sessions.on': True,
		'tools.staticdir.root': os.getcwd()
	},
	"/css":{
		'tools.staticdir.on':True,
		'tools.staticdir.dir':"freeboard/css"
	},
	"/js":{
		'tools.staticdir.on':True,
		'tools.staticdir.dir':"freeboard/js"
	},
	"/img":{
		'tools.staticdir.on':True,
		'tools.staticdir.dir':"freeboard/img"
	},
	"/plugins":{
		'tools.staticdir.on':True,
		'tools.staticdir.dir':"freeboard/plugins"
	},
	"/dashboard":{
		'tools.staticdir.on':True,
		'tools.staticdir.dir':"freeboard/dashboard"
	}
}


cherrypy.tree.mount(WebApp(), "/", conf)


cherrypy.server.socket_port = 8080

cherrypy.engine.start()
cherrypy.engine.block()
