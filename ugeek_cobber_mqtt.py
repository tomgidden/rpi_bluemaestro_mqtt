#!/usr/bin/env python3
# -*- coding: utf-8 -*-

mqtt_host = '192.168.0.2'

import paho.mqtt.client as paho

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from bme280 import BME280
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


topic = '/sensor/uk/CB29JW/inside'

humidity_calibrate = 0
pressure_calibrate = 0
temperature_calibrate = 0
lux_calibrate = 0

frequency = 3

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

    bus = SMBus(1)

    try:
        while exiting is None:
            try:
                print ("Connecting")

                i2c_lock()
                bme_address = 0x77
                apds_address = 0x39

                apds = None
                bme = None

                try:
                    GPIO.setmode(GPIO.BOARD)
                    GPIO.setup(7, GPIO.IN)
                    #GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)

                    apds = APDS9960(bus)
                    apds.enableLightSensor()
                    lux = apds.readAmbientLight()
                except IOError as e:
                    print (e)

                try:
                    bme = BME280(i2c_dev=bus, i2c_addr=bme_address)
                    bme.update_sensor()
                except IOError as e:
                    print (e)

                i2c_unlock()

                time.sleep(frequency)

                while exiting is None:
                    i2c_lock()

                    mqtt.publish(topic + '/watchdog', 'reset', retain=False)
 #                   print ("{}/watchdog: reset".format(topic))

                    now = time.time()
                    timestamp = int(now)

                    if apds is not None:
                        try:
                            short_delay = True
                            lux = apds.readAmbientLight()
                            if lux:
                                lux = lux + lux_calibrate
                                mqtt.publish(topic + '/luminosity', lux, retain=True)
                                mqtt.publish(topic + '/luminosity/timestamp', timestamp, retain=True)
#                                print("{} lux".format(lux))
                                short_delay = False
                        except IOError as e:
                            print (e)


                    if bme is not None:
                        try:
                            bme.update_sensor()


                            bme_data = bme.__dict__

                            mqtt.publish(topic + '/humidity', bme_data['humidity'], retain=True)
                            mqtt.publish(topic + '/humidity/timestamp', timestamp, retain=True)
                            mqtt.publish(topic + '/pressure', bme_data['pressure'], retain=True)
                            mqtt.publish(topic + '/pressure/timestamp', timestamp, retain=True)
                            mqtt.publish(topic + '/temperature', bme_data['temperature'], retain=True)
                            mqtt.publish(topic + '/temperature/timestamp', timestamp, retain=True)
#                            print("{}ºC\t{} %rH\t{} hPa".format(bme_data['temperature'], bme_data['humidity'], bme_data['pressure']))
                            short_delay = False
                        except IOError as e:
                            print (e)

                    i2c_unlock()

                    if short_delay:
                        time.sleep(1)
                    else:
                        time.sleep(frequency)

            except IOError as e:
                print (e)
                i2c_unlock()
                time.sleep(3)

    except KeyboardInterrupt:
        pass


    sys.exit(exiting)

except KeyboardInterrupt:
    sys.exit(0)
