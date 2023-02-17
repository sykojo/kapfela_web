from flask import Blueprint
import time
import paho.mqtt.client as mqtt
from time import time_ns


class InstrumentAlive():
    def __init__(self):
        self.current_time = time_ns() + 3600000000000
        self.instruments_list = ["uku","cajon","vizualizace","bass","guitar"]
        self.states_list = ['-',self.current_time]
        self.instruments = {}
        self._client = mqtt.Client()
        self.functions_of_instruments = ["send_status",
                                         "send_time"]
        
        '''Creating a table with all instruments and their statuses'''
        for instrument in self.instruments_list:
            self.instruments[instrument] = self.states_list
        
        self.NTP_EPOCH_OFFSET = 946684800000000000
        self.MAX_TIME_DIFFERENCE = 30000000000#ns -> 30s
        
    
    def _mqtt_subscribe(self):
        """Subscribe to all instruments and their functions"""
        for instrument in self.instruments:
            for function in self.functions_of_instruments:
                self._client.subscribe(f"kapfela/{instrument}/{function}") 
                print(f"Subscribed to topic: kapfela/{instrument}/{function} \n")   
    
    def mqtt_on_connect(self, client, userdata, flags, rc):      
        self._mqtt_subscribe()
           

    def mqtt_on_message(self, client, userdata, msg):    
        """MQTT Topics Handler"""    
        topic = str(msg.topic)
        if topic.startswith("kapfela/"):
            instrument = topic.split("/")[1]
            function = topic.split("/")[2]
            message = str(msg.payload.decode("utf-8"))
            
            '''Depending on what topic comes to handler, it determines what function on what instrument to run '''    
            if function == "send_status":
                self.instruments[instrument][0] = message #Status change
                
            elif function == "send_time":
                self.instruments[instrument][1] = message #Time change
    

    def mqtt_on_publish(self, client, userdata, result):
        print(" A message has been published! ")
        return True

    def start(self):
        """Creates MQTT Client, defines callback functions, connects to mqtt broker and creates a loop"""
        try:    
            self._client.on_connect = self.mqtt_on_connect
            self._client.on_message = self.mqtt_on_message
            self._client.connect("localhost", 1883, 60)
            self._client.loop_start()
            return True
        except:
            print("Alive se nepodařilo inicializovat!")
            return False
       
    

