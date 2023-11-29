import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
from paho.mqtt import client as mqtt_client



class MessageHandler:
    # self.client is the mqtt client from main

    def __init__(self):
        load_dotenv()
        self.url: str = os.getenv("SUPABASE_URL")
        self.key: str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.url, self.key)
    
    def setClient(self, client: mqtt_client.Client):
        self.client = client

    def messageReceive(self, topic: str, payload: str):
        parts = topic.split("/")
        main_topic = parts[0]
        sub_topic = parts[1]
        print(parts[0])

        if(main_topic == "light-controller"):
            # light controller stuff
            print(f'Message recieved in light-controller (sub topic: {sub_topic})')
            # self.client.publish("companions/python-res", "hello!")
            print(payload)
        elif(main_topic == "companions"):
            # companions stuff
            print(f'Message recieved in companions (sub topic: {sub_topic})')
            print(payload)
        else:
            # un classified stuff
            print(f'Unclassified message received {sub_topic}')
            print(payload)

    def testDB(self):
       data, count = self.supabase.table('test_table').insert({
           "topic": "test",
           "sub_topic": "test",
           "message": "test message"
       }).execute()
       print("data ", data)
       print("count ", count)

    def companions_message(sub_topic):
        pass

    def light_controller_message(sub_topic):
        pass






