#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paho.mqtt.client as paho
import BlueMaestro
import time
import fcntl
import base64

mqtt_host = os.environ['MQTT_HOST']
topic = os.environ['MQTT_TOPIC']
client_name = os.environ['MQTT_CLIENT_NAME']

temperature_calibrate = 0
frequency = 1

mqtt = paho.Client(client_name)

def on_disconnect(mqtt, userdata, rc):
    print("Disconnected from MQTT server with code: %s" % rc)
    print(userdata)
    while rc != 0:
        try:
            time.sleep(1)
            rc = mqtt.reconnect()
        except:
            pass
        print("Reconnected to MQTT server.")

mqtt.on_disconnect = on_disconnect
mqtt.connect(mqtt_host, 1883, 60)
mqtt.loop_start()


def callback(data):
    now = time.time()
    timestamp = int(now)
    if 'data' in data: data['data'] = base64.b64encode(data['data'])
    print (data)

    try:
        mqtt.publish('{}/{}/watchdog'.format(topic, data['name']), 'reset', retain=False)
        for k, v in data.items():
            mqtt.publish('{}/{}/{}'.format(topic, data['name'], k), v, retain=False)
            mqtt.publish('{}/{}/{}/timestamp'.format(topic, data['name'], k), timestamp, retain=False)
    except ValueError as e:
        print (e)
        print (data)


try:
    while True:
        try:
            sensor = BlueMaestro.init()
            BlueMaestro.get(sensor, callback)
            time.sleep(frequency)

        except IOError as e:
            print("IOError: "+str(e))
            time.sleep(3)

except KeyboardInterrupt:
    pass
