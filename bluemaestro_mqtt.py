#!/usr/bin/env python3
# -*- coding: utf-8 -*-

mqtt_host = os.environ['MQTT_HOST']
topic = os.environ['MQTT_TOPIC']
client_name = os.environ['MQTT_NAME']

import paho.mqtt.client as paho
import BlueMaestro
import time
import fcntl
import os


temperature_calibrate = 0
frequency = 60

def on_disconnect(mqtt, userdata, rc):
    print("Disconnected from MQTT server with code: %s" % rc)
    while rc != 0:
        try:
            time.sleep(1)
            rc = mqtt.reconnect()
        except:
            pass
        print("Reconnected to MQTT server.")

mqtt = paho.Client(client_name)

mqtt.connect(mqtt_host, 1883, 60)
mqtt.on_disconnect = on_disconnect
mqtt.loop_start()

try:
    while True:
        try:
            sensor = BlueMaestro.init()
            data = BlueMaestro.get(sensor)
            print (data)
            if data is not None:
                data['time'] = time.strftime('%Y-%m-%d %H:%M:%S')

                now = time.time()
                timestamp = int(now)
                mqtt.publish(topic + '/watchdog', 'reset', retain=False)

                if 'humidity' in data:
                    mqtt.publish(topic + '/humidity', data['humidity'], retain=True)
                    mqtt.publish(topic + '/humidity/timestamp', timestamp, retain=True)

                if 'pressure' in data:
                    mqtt.publish(topic + '/pressure', data['pressure'], retain=True)
                    mqtt.publish(topic + '/pressure/timestamp', timestamp, retain=True)

                if 'temperature' in data:
                    mqtt.publish(topic + '/temperature', data['temperature'] + temperature_calibrate, retain=True)
                    mqtt.publish(topic + '/temperature/timestamp', timestamp, retain=True)

            else:
                print("No data yet.")

            time.sleep(frequency)

        except IOError as e:
            print("IOError: "+str(e))
            time.sleep(3)

except KeyboardInterrupt:
    pass
