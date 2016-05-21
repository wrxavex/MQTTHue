#!/usr/bin/python
from phue import Bridge
import random
import logging
from time import sleep
logging.basicConfig()

b = Bridge('192.168.1.178', 'YxPYRWNawywC-sKHkjuRho7iOwMMSrn3di2ETF74') # Enter bridge IP here.

#If running for the first time, press button on bridge and run with b.connect() uncommented
#b.connect()

lights = b.get_light_objects()
#while 1:
#	for light in lights:
#		light.brightness = random.randint(0,1)
		#light.xy = [random.random(),random.random()]
#		light.hue = random.randint(38000, 44000)
#		light.saturation = random.randint(0,255)
#			light.hue = 2048*i
#			sleep(0.4)
#	sleep(random.uniform(0.1,1))

while 1:
	# for light in lights:
	# 	if random.randint(1,5) > 2:
	# 		light.on = True
	# 		light.saturation = 254
	# 		light.brightness = 254
	# 		light.hue = random.randint(44000, 48000)
	# 	else:
	# 		light.on = False
	for color in range(1,20):
		lights[1].hue = 1000+3000*color
		lights[1].saturation = 255
		print (lights[1].hue)
		for bri in range(0,255, 8):
			lights[1].brightness = bri
			print (bri)
			sleep(random.uniform(0.01,0.2))
		for bri in range(255,0, -8):
			lights[1].brightness = bri
			print (bri)
			sleep(random.uniform(0.01, 0.2))
	
