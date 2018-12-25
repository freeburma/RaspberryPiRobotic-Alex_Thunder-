#! /usr/bin/python
import RPi.GPIO as GPIO
import time

'''
This code is working and tested on 
13-Oct-2018 10:24 pm Satursday 

From the Addept Learning Tutorial, sometimes stop and is not detecting the distance. Not reliable. 
'''

def checkdist():
	GPIO.output(16, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(16, GPIO.LOW)
	while not GPIO.input(18):
		pass
	t1 = time.time()
	while GPIO.input(18):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(18,GPIO.IN)
time.sleep(2)
try:
	while True:
		print ('Distance: %0.2f cm : %0.2f m' %(checkdist()*100, checkdist()))
		time.sleep(0.5)
except KeyboardInterrupt:
	GPIO.cleanup()


