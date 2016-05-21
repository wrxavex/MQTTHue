#!/usr/bin/python
from phue import Bridge
import random
import logging
from time import sleep
import json
import thread
import sys

try:
    import paho.mqtt.client as mqtt
except ImportError:
    import os
    import inspect

    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt

D6T_blocks = ""
lightrunning = {1:False, 2:False, 3:False}

class MyMQTTClass:
    def __init__(self, clientid=None):
        self._mqttc = mqtt.Client(clientid)
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe

    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def mqtt_on_message(self, mqttc, obj, msg):
        global D6T_blocks

        if "Blocks" in msg.topic:
            D6T_blocks = str(msg.payload)
            # print (D6T_blocks)

        # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def mqtt_on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def mqtt_on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        self._mqttc.connect("www.znh.tw", 1883, 60)
        self._mqttc.subscribe("/#", 0)

        rc = 0
        while rc == 0:
            rc = self._mqttc.loop()
        return rc

lock = thread.allocate_lock()



logging.basicConfig()

b = Bridge('192.168.1.178', 'YxPYRWNawywC-sKHkjuRho7iOwMMSrn3di2ETF74')  # Enter bridge IP here.

# If running for the first time, press button on bridge and run with b.connect() uncommented
# b.connect()

lights = b.get_light_objects()

# while 1:
# 	for light in lights:
# 		light.brightness = random.randint(0,1)
# light.xy = [random.random(),random.random()]
# 		light.hue = random.randint(38000, 44000)
# 		light.saturation = random.randint(0,255)
# 			light.hue = 2048*i
# 			sleep(0.4)
# 	sleep(random.uniform(0.1,1))

# while 1:
#     # for light in lights:
#     # 	if random.randint(1,5) > 2:
#     # 		light.on = True
#     # 		light.saturation = 254
#     # 		light.brightness = 254
#     # 		light.hue = random.randint(44000, 48000)
#     # 	else:
#     # 		light.on = False
#     for color in range(1, 20):
#         lights[1].hue = 1000 + 3000 * color
#         lights[1].saturation = 255
#         print(lights[1].hue)
#         for bri in range(0, 255, 8):
#             lights[1].brightness = bri
#             print(bri)
#             sleep(random.uniform(0.01, 0.2))
#         for bri in range(255, 0, -8):
#             lights[1].brightness = bri
#             print(bri)
#             sleep(random.uniform(0.01, 0.2))
def lights_init():
    global lights
    print ('light init')
    for light in range(1,4):
        print ('init%d' % light)
        if b.get_light(light, 'on') == True:
            print ('init%d' % light )
            b.set_light(light, 'on', False)

def show_on(light, *args):
    global lights
    slow_on = {'transitiontime': 50, 'on': True, 'bri': 254}
    b.set_light(light, slow_on)
    sleep(15)
    b.set_light(light, 'on', False)
    lightrunning[light] = False


def light_updater():
    global lights
    global D6T_blocks
    global lightrunning
    print (D6T_blocks)
    D6T_json = json.loads(D6T_blocks)
    # print ("mom I'm here")
    if (D6T_json["13"] == "1"):
        # if lightrunning[1] == False:
        #     lightrunning[1] = True
        if b.get_light(1, 'on') == False:
            print("light 1 ready to on")
            thread.start_new_thread(show_on, (1, lock))
    if (D6T_json["10"] == "1"):
        # if lightrunning[2] == False:
        #     lightrunning[2] = True
        if b.get_light(2, 'on') == False:
            print("light 2 ready to on")
            thread.start_new_thread(show_on, (2, lock))
    if (D6T_json["11"] == "1"):
        # if lightrunning[3] == False:
        #     lightrunning[3] = True
        if b.get_light(3, 'on') == False:
            print("light 3 ready to on")
            thread.start_new_thread(show_on, (3, lock))






def get_MQTT(sleeptime, *args):
    global MQTT_rc
    mqttc = MyMQTTClass()
    MQTT_rc = mqttc.run()


def main():
    global D6T_blocks

    lights_init()


    thread.start_new_thread(get_MQTT, ("", lock))


    while True:
        sleep(1)
        light_updater()








if __name__ == '__main__':
    print ("MQTTHue start")
    main()