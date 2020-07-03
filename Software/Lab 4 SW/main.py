from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
import time
import json
import requests
import threading
from Subscriber import Subscriber
from Publisher import Publisher
class MainApp(App):

    def build(self):
        self.autoSystem_on=False
        self.presenceTMH = None
        self.presenceTmH = None
        self.presenceNTMH = None
        self.presenceNTmH = None
        self.presenceTMF = None
        self.presenceTmF = None
        self.presenceNTMF = None
        self.presenceNTmF = None 
        self.main_layout = BoxLayout(orientation="vertical")
        self.Title = Label(text='Smart House Controller',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .9})
        self.main_layout.add_widget(self.Title)
        self.temperature_layout=BoxLayout(orientation="horizontal")
        self.Temperature = Label(text='Temperature :',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .9, 'center_y': .5})
        self.Temperature_data = TextInput(
                                            multiline=False,
                                            readonly=True,
                                            halign="left",
                                            font_size=20,
                                            background_color=[0,0,0,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[1,1,1,1]
                                        )
        self.temperature_layout.add_widget(self.Temperature)
        self.temperature_layout.add_widget(self.Temperature_data)
       
        self.presence_layout=BoxLayout(orientation="horizontal")
        self.Presence = Label(text='Presence :',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .9, 'center_y': .5})
        self.Presence_data = TextInput(
                                            multiline=False,
                                            readonly=True,
                                            halign="left",
                                            font_size=20,
                                            background_color=[0,0,0,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[1,1,1,1]
                                        )
        self.temperature_layout.add_widget(self.Presence)
        self.temperature_layout.add_widget(self.Presence_data)
        self.main_layout.add_widget(self.temperature_layout)
        self.check_layout=BoxLayout(orientation="horizontal")
        self.auto = Label(text='Automatic',
                      font_size='20sp',
                      size_hint=(10, .2),
                      pos_hint={'center_x': -20.0, 'center_y': .5})
        self.checkbox = CheckBox()
        self.checkbox.bind(active=self.on_checkbox_active)
        self.check_layout.add_widget(self.checkbox)
        self.check_layout.add_widget(self.auto)
        self.main_layout.add_widget(self.check_layout)
        self.slider_layout=BoxLayout(orientation="horizontal")
        self.fan = Label(text='Fan',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.fan_s = Slider(min=0, max=255, value=0)
        self.heat = Label(text='Heater',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.heat_s = Slider(min=0, max=255, value=0)
        self.slider_layout.add_widget(self.fan)
        self.slider_layout.add_widget(self.fan_s)
        self.slider_layout.add_widget(self.heat)
        self.slider_layout.add_widget(self.heat_s)
        self.main_layout.add_widget(self.slider_layout)
        self.option_layout=BoxLayout(orientation="vertical")
        self.presT_layout=BoxLayout(orientation="horizontal")
        self.NpresT_layout=BoxLayout(orientation="horizontal")
        self.Option_title= Label(text='Automatic control value of temperature',
                      font_size='20sp',
                      size_hint=(.5, .8),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.presT_title= Label(text='With Presence',
                      font_size='20sp',
                      size_hint=(.5, .8),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.NpresT_title= Label(text='Without Presence',
                      font_size='20sp',
                      size_hint=(.5, .8),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MAX1H= Label(text='MAX',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MIN1H=Label(text='Heater MIN',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MAX1F= Label(text='MAX',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MIN1F=Label(text='Fan MIN',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MAX2H= Label(text='MAX',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MIN2H=Label(text='Heater MIN',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MAX2F= Label(text='MAX',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.MIN2F=Label(text='Fan MIN',
                      font_size='20sp',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.presT_dataMH = TextInput(
                                            multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                            
                                        )
        self.presT_dataMH.bind(text=self.on_textPMH)
        self.presT_datamH = TextInput(       multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                        )
        self.presT_datamH.bind(text=self.on_textPmH)
        self.presT_layout.add_widget(self.MIN1H)
        self.presT_layout.add_widget(self.presT_datamH)
        self.presT_layout.add_widget(self.MAX1H)
        self.presT_layout.add_widget(self.presT_dataMH)
        self.presT_dataMF = TextInput(
                                          multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                            
                                        )
        self.presT_dataMF.bind(text=self.on_textPMF)
        self.presT_datamF = TextInput(       multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                        )
        self.presT_datamF.bind(text=self.on_textPmF)
        self.presT_layout.add_widget(self.MIN1F)
        self.presT_layout.add_widget(self.presT_datamF)
        self.presT_layout.add_widget(self.MAX1F)
        self.presT_layout.add_widget(self.presT_dataMF)
        self.NpresT_dataMH = TextInput(
                                            multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                        )
        self.NpresT_dataMH.bind(text=self.on_textNPMH)
        self.NpresT_datamH = TextInput(  multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                        )
        self.NpresT_datamH.bind(text=self.on_textNPmH)
        self.NpresT_layout.add_widget(self.MIN2H)
        self.NpresT_layout.add_widget(self.NpresT_datamH)
        self.NpresT_layout.add_widget(self.MAX2H)
        self.NpresT_layout.add_widget(self.NpresT_dataMH)
        self.NpresT_dataMF = TextInput(
                                            multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                        )
        self.NpresT_dataMF.bind(text=self.on_textNPMF)
        self.NpresT_datamF = TextInput(  multiline=False,
                                            halign="right",
                                            font_size=15,
                                            size_hint=(.35,1),
                                            background_color=[1,1,1,1],
                                            cursor_blink=False,
                                            cursor_color=[0,0,0,1],
                                            selection_color=[0,0,0,0],
                                            #padding_y=29,
                                            foreground_color=[0,0,0,1]
                                        )
        self.NpresT_datamF.bind(text=self.on_textNPmF)
        self.NpresT_layout.add_widget(self.MIN2F)
        self.NpresT_layout.add_widget(self.NpresT_datamF)
        self.NpresT_layout.add_widget(self.MAX2F)
        self.NpresT_layout.add_widget(self.NpresT_dataMF)
        self.option_layout.add_widget(self.Option_title)
        self.option_layout.add_widget(self.presT_title)
        self.option_layout.add_widget(self.presT_layout)
        self.option_layout.add_widget(self.NpresT_title)
        self.option_layout.add_widget(self.NpresT_layout)

        self.button = Button(

                    text="launch autonomous system",

                    pos_hint={"center_x": 0.5, "center_y": 0.5},

                )

        self.button.bind(on_release=self.on_button_press)
        self.option_layout.add_widget(self.button)


        return self.main_layout
    def on_button_press(self,instance):
        if self.presenceTMH != None and self.presenceTmH != None and self.presenceNTMH != None and self.presenceNTmH != None and  self.presenceTMF != None and self.presenceTmF != None and self.presenceNTMF != None and self.presenceNTmF != None :
            if  self.autoSystem_on==False :
                self.autoSystem_on=True
                instance.background_color=[0,1,0,1]
                instance.text="Launched"
            else:
                self.autoSystem_on=False
                instance.background_color=[1,1,1,1]
                instance.text="launch autonomous system"
        else:
            instance.background_color=[1,0,0,1]
        
    def on_textPMH(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceTMH=val
        else :
            instance.text=""
            self.presenceTMh=None
    def on_textPmH(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceTmH=val
        else :
            instance.text=""
            self.presenceTmH=None
    def on_textPMF(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceTMF=val
        else :
            instance.text=""
            self.presenceTMF=None
    def on_textPmF(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceTmF=val
        else :
            instance.text=""
            self.presenceTmF=None
    def on_textNPMH(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceNTMH=val
        else :
            instance.text=""
            self.presenceNTMH=None
    def on_textNPmH(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceNTmH=val
        else :
            instance.text=""
            self.presenceNTmH=None
    def on_textNPMF(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceNTMF=val
        else :
            instance.text=""
            self.presenceNTMF=None
    def on_textNPmF(self,instance, value):
        val,ok=self.isFloat(value)
        if ok:
            self.presenceNTmF=val
        else :
            instance.text=""
            self.presenceNTmF=None

    

    def isFloat(self,s):
        try:
            return float(s),True
        except ValueError:
            return 0,False


    def on_checkbox_active(self,checkbox, value):
        if value:
            self.fan_s.disabled=True
            self.heat_s.disabled=True
            self.main_layout.add_widget(self.option_layout)
            if self.presenceTMH != None and self.presenceTmH != None and self.presenceNTMH != None and self.presenceNTmH != None and  self.presenceTMF != None and self.presenceTmF != None and self.presenceNTMF != None and self.presenceNTmF != None :
              self.presT_dataMH.text=str( self.presenceTMH)
              self.presT_datamH.text= str(self.presenceTmH)
              self.NpresT_dataMH.text=str(self.presenceNTMH)
              self.NpresT_datamH.text= str(self.presenceNTmH)
              self.presT_dataMF.text=str( self.presenceTMF)
              self.presT_datamF.text= str(self.presenceTmF)
              self.NpresT_dataMF.text=str(self.presenceNTMF)
              self.NpresT_datamF.text= str(self.presenceNTmF) 
        else:
            self.fan_s.disabled=False
            self.heat_s.disabled=False
            self.main_layout.remove_widget(self.option_layout)
            self.autoSystem_on=False
            
    
    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
            # A new message is received
          
            body=msg.payload.decode("utf-8")
            print(body)
            js=json.loads(body)
            self.Temperature_data.text ="Temperature: "+ str(js['temperature'])+" "+js['unit']
            self.temperature=js['temperature']
            self.Presence_data.text="Presence: "+str(js['presence'])
            self.presence=js['presence']
 
    def automatic_system(self,dt):
        diz={
                  "Fan":None,
                  "Heat":None}
        if self.autoSystem_on==False :
            diz['Fan']=self.fan_s.value
            diz['Heat']=self.heat_s.value
        else:
            if self.presence:
                diz['Fan']=int(((self.presenceTMF-self.presenceTmF)/255)*self.temperature)
                
                diz['Heat']=int(255-((self.presenceTMH-self.presenceTmH)/255)*self.temperature)
            else:
                diz['Fan']=int(((self.presenceNTMF-self.presenceNTmF)/255)*self.temperature)
                diz['Heat']=int(255-((self.presenceNTMH-self.presenceNTmH)/255)*self.temperature)
       
        if  diz['Fan']>255:
                     diz['Fan']=255
        if  diz['Fan']<0:
                     diz['Fan']=0
        if  diz['Heat']>255:
                     diz['Heat']=255
        if  diz['Heat']<0:
                     diz['Heat']=0
      
        test= Publisher("MyPublisher",broker)
        test.start()
        test.myPublish ('/tiot/17/house/control',json.dumps(diz))

        test.stop()

            
def sendData(dt):         
    load=json.dumps({
              "ID": "Smart_House",
              "Description":"Control the smart house",
              "endPoint":"/Mqtt/control",
            })
    requests.put('http://localhost:8080/service/', data=load) 

if __name__ == '__main__':
    app = MainApp()
    Clock.schedule_once(sendData)
    Clock.schedule_interval(sendData, 60)
    broker=requests.get('http://localhost:8080/broker/')
    broker=broker.json()
    s='http://localhost:8080/device/one?ID=house'

    topic=requests.get(s)
    
    topic=topic.json()
  
    sensSub=Subscriber("Temperature",broker,topic['endPoint'],app.myOnMessageReceived)
    sensSub.start()
 
    test= Publisher("MyPublisher",broker)
    test.start()
    test.myPublish ('/tiot/17/house/control',json.dumps(diz))
    test.stop()
    Clock.schedule_interval(app.automatic_system, 20)
    app.run()

        

   
