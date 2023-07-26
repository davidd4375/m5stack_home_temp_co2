import os, sys, io
import M5
from M5 import *
from hardware import *
from umqtt import *
import time
from unit import *


i2c0 = None
mqtt_client = None
env3_0 = None


temp = None
msg = None
room = None


def setup():
  global i2c0, mqtt_client, env3_0, temp, msg, room

  i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
  env3_0 = ENV(i2c=i2c0, type=3)
  M5.begin()
  mqtt_client = MQTTClient('hellom5', 'm5server.local', port=1883, user='atom1', password='test4375', keepalive=300)
  mqtt_client.connect(clean_session=True)
  room = ' office'


def loop():
  global i2c0, mqtt_client, env3_0, temp, msg, room
  temp = env3_0.read_temperature()
  temp = temp * 1.8
  temp = temp + 32
  msg = (str(temp)) + room
  mqtt_client.publish('temp', msg, qos=0)
  time.sleep(2)


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
