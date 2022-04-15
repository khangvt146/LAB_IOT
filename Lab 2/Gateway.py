import paho.mqtt.client as mqttclient
import time
import json
import random

BROKER_ADDRESS = "mqttserver.tk"
PORT = 1883


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    # temp_data = {'value': True}
    # try:
    #     jsonobj = json.loads(message.payload)
    #     if jsonobj['method'] == "setValue":
    #         temp_data['value'] = jsonobj['params']
    #         client.publish('/bkiot/1913713/status', json.dumps(temp_data), 1)
    # except:
    #     pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Sever connected successfully!!")
        client.subscribe("/bkiot/1913713/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Station 1")
client.username_pw_set('bkiot', '12345678')
client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

# choice = ['ON', 'OFF']
led_toggle = {'device': 'LED', 'status': 'OFF'}
pump_toggle = {'device': 'PUMP', 'status': 'OFF'}

while True:
    temp = random.randint(20, 40)
    humid = random.randint(10, 100)
    collect_data = {'temperature': temp, 'humidity': humid}
    # led_toggle = {'device': 'LED', 'status': choice[random.randint(0,1)]}
    # pump_toggle = {'device': 'PUMP', 'status': choice[random.randint(0,1)]}
    client.publish('/bkiot/1913713/status', json.dumps(collect_data), 1)
    # client.publish('/bkiot/1913713/led', json.dumps(led_toggle), 1)
    # client.publish('/bkiot/1913713/pump', json.dumps(pump_toggle), 1)
    time.sleep(10)

