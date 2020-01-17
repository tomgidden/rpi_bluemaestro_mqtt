#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paho.mqtt.client as paho
import BlueMaestro
import time
import fcntl

mqtt_host = os.environ['MQTT_HOST']
topic = os.environ['MQTT_TOPIC']
client_name = os.environ['MQTT_CLIENT_NAME']

temperature_calibrate = 0
frequency = 60

mqtt = paho.Client(client_name)

def on_disconnect(mqtt, userdata, rc):
    print("Disconnected from MQTT server with code: %s" % rc)
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

try:
    while True:
        try:
            sensor = BlueMaestro.init()
            data = BlueMaestro.get(sensor)

            if data is not None:

                now = time.time()
                timestamp = int(now)

                print (data)

                mqtt.publish(topic + '/watchdog', 'reset', retain=False)

                for k, v in data.items():
                    mqtt.publish('{}/{}'.format(topic, k), v, retain=True)
                    mqtt.publish('{}/{}/timestamp'.format(topic, k), timestamp, retain=True)

                time.sleep(frequency)

            else:
                print("No data yet.")
                time.sleep(5)


        except IOError as e:
            print("IOError: "+str(e))
            time.sleep(3)

except KeyboardInterrupt:
    pass
