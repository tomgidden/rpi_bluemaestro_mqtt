#!/usr/bin/env python3
# -*- coding: utf-8 -*-

mqtt_host = '192.168.7.2'

import paho.mqtt.client as paho

import smbus2
import bme280

from apds9960 import APDS9960
from apds9960.const import *

import RPi.GPIO as GPIO

import time
import fcntl
import socket
import signal
import sys

from i2c_lock import i2c_lock, i2c_unlock

exiting = None

host = socket.gethostname()


topic = '/sensor/{}'.format(host)

humidity_calibrate = 0
pressure_calibrate = 0
temperature_calibrate = 0
lux_calibrate = 0

frequency = 3

bus = smbus2.SMBus(1)

def on_disconnect(mqtt, userdata, rc):
    print("Disconnected from MQTT server with code: %s" % rc)
    while rc != 0:
        try:
            time.sleep(1)
            rc = mqtt.reconnect()
        except:
            pass
        print("Reconnected to MQTT server.")

mqtt = paho.Client()


try:
    def shutdown_handler(signum, frame):
        print("Setting exiting to 0")
        exiting = 0

    def restart_handler(signum, frame):
        print("Setting exiting to -1")
        exiting = 255

    signal.signal(signal.SIGUSR1, restart_handler)

    mqtt.connect(mqtt_host, 1883, 60)
    mqtt.on_disconnect = on_disconnect
    mqtt.loop_start()

    try:
        while exiting is None:
            try:
                i2c_lock()
                bme_address = 0x77
                apds_address = 0x39

                bme_calibration_params = bme280.load_calibration_params(bus, bme_address)
                apds = APDS9960(bus)
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(7, GPIO.IN)
                #GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)
                apds.enableLightSensor()

                i2c_unlock()

                while exiting is None:
                    i2c_lock()
                    bme_data = bme280.sample(bus, bme_address, bme_calibration_params)
                    lux = apds.readAmbientLight()

                    mqtt.publish(topic + '/watchdog', 'reset', retain=False)
                    now = time.time()
                    timestamp = int(now)

                    short_delay = True
                    if lux:
                        lux = lux + lux_calibrate
                        mqtt.publish(topic + '/luminosity', lux, retain=True)
                        mqtt.publish(topic + '/luminosity/timestamp', timestamp, retain=True)
                        #print("{} lux".format(lux))
                        short_delay = False

                    if bme_data:
                        mqtt.publish(topic + '/humidity', bme_data.humidity + humidity_calibrate, retain=True)
                        mqtt.publish(topic + '/humidity/timestamp', timestamp, retain=True)
                        mqtt.publish(topic + '/pressure', bme_data.pressure + pressure_calibrate, retain=True)
                        mqtt.publish(topic + '/pressure/timestamp', timestamp, retain=True)
                        mqtt.publish(topic + '/temperature', bme_data.temperature + temperature_calibrate, retain=True)
                        mqtt.publish(topic + '/temperature/timestamp', timestamp, retain=True)
                        #print("{}ºC\t{} %rH\t{} hPa".format(bme_data.temperature, bme_data.humidity, bme_data.pressure))
                        short_delay = False

                    i2c_unlock()

                    if short_delay:
                        time.sleep(1)
                    else:
                        time.sleep(frequency)

            except IOError as e:
                print("IOError: "+str(e))
                i2c_unlock()
                time.sleep(3)

    except KeyboardInterrupt:
        pass


    sys.exit(exiting)

except KeyboardInterrupt:
    sys.exit(0)
