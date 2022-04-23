import paho.mqtt.client as mqttclient
import time
import json

import serial.tools.list_ports

mess = ""
bbc_port = "COM6"
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "kvOBWfYtgAYJ9E6TV0hn"


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    #TO DO


def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end + 1:]


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        # if jsonobj['method'] == "setValue":
        if jsonobj['method'] == "setLED":
            temp_data['value_LED'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        if jsonobj['method'] == "setPump":
            temp_data['value_PUMP'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)

    except:
        pass

    if len(bbc_port) > 0:
        ser.write((str("khangne") + "#").encode())


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intensity = 100
counter = 0

longitude = 108.446756
latitude = 11.9536685
while True:
    # if len(bbc_port) > 0:
    #     readSerial()
    collect_data = {'temperature': temp, 'light': humi}
    client.publish('v1/devices/me/attributes', json.dumps(collect_data), 1)
    temp += 1
    humi += 1
    time.sleep(20)
