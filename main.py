from paho.mqtt import client as mqtt_client
import time
from messages import MessageHandler
import os
from dotenv import load_dotenv

load_dotenv()

broker = os.getenv("MQTT_URL")
port = 8883 # mqtt port
# wsPort = 8084 # ws port
client_id = "python-mqtt"
username = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PW")

message_handler = MessageHandler()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("MQTT Connected.")
        else:
            print("Failed connection, return code %d\n", rc)
    # connect client ID
    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs='./emqxsl-ca.crt')
    client.username_pw_set(username,password)
    client.on_connect = on_connect
    client.connect(broker, port)
    message_handler.setClient(client)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message_handler.messageReceive(msg.topic, msg.payload.decode())

    client.subscribe("light-controller/#", qos=0)
    client.subscribe("companions/#", qos=0)
    client.on_message = on_message

def test_publish(client):
    topic = "light-controller/python"
    msg_count = 0

    result = client.publish(topic, "Hello")
        # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Sent to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")



def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()