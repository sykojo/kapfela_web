from flask import Blueprint
import time
import paho.mqtt.client as mqtt
from time import time_ns
import json
import requests
from time import sleep


class InstrumentAlive():
    def __init__(self):
        self.json_file = "db/instruments.json"
        self.current_time = time_ns() + 3600000000000 
        self.instruments = []
        self._client = mqtt.Client()
        self.functions_of_instruments = ["send_status",
                                         "send_time"]
        '''Creating a table with all instruments and their statuses from json file'''
        with open(self.json_file,"r") as f:
            data = json.load(f)
            for instrument_data in data:
                instrument = {
                    "name": instrument_data["name"],
                    "status": instrument_data["state"],
                    "time": self.current_time
                }
                self.instruments.append(instrument)
        
        
        
        self.NTP_EPOCH_OFFSET = 946684800000000000
        self.MAX_TIME_DIFFERENCE = 30000000000#ns -> 30s
        
    
    def _mqtt_subscribe(self):
        """Subscribe to all instruments and their functions"""
        for instrument_data in self.instruments:
            for function in self.functions_of_instruments:
                instrument = instrument_data["name"]  
                self._client.subscribe(f"kapfela/{instrument}/{function}")
                print(f"Subscribed to topic: kapfela/{instrument}/{function}")
                
    def get_instrument_names(self):
        instruments_names_list = []
        for instrument in self.instruments:
            instruments_names_list.append(instrument["name"])
        return instruments_names_list 
                
            
    def update_instruments_table(self,instrument,data_type,msg):
        for instrument_data in self.instruments:
            if instrument_data["name"] == instrument:
                instrument_data[data_type] = msg
                break
            
    def update_json(self, instrument, msg):
        with open(self.json_file, "r+") as f:
            data = json.load(f)
            for instrument_data in data:
                if instrument_data["name"] == instrument:
                    instrument_data["state"] = msg
                    break
            f.seek(0)
            json.dump(data, f)
            f.truncate()
    
    def get_status_from_json(self,instrument):
        with open(self.json_file,"r") as f:
            data = json.load(f)
            for instrument_data in data:
                if instrument_data["name"] == instrument:
                    status = instrument_data["state"]
                    break
        return status
    '''
    def update_status_on_web(self):
        while True:
            for instrument in self.get_instrument_names():
                url = "update/update_status/" + instrument
                status = requests.get(url) 
            
            sleep(1)#second
    '''
    
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
                self.update_json(instrument,message)
                self.update_instruments_table(instrument,"state",message)
                
            elif function == "send_time":
                self.update_instruments_table(instrument,"time",message)
    

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
       
    

