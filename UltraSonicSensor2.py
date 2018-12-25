import RPi.GPIO as GPIO
import time 

'''
This code is working and tested on 
13-Oct-2018 10:24 pm Satursday 

Reference Url: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
'''

GPIO.setmode(GPIO.BOARD)

# Set GPIO Pins 
GPIO_TRIGGER = 16
GPIO_ECHO = 18

# Set GPIO directin (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance(): 
	# Set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
	
	# Set Trigger after 0.01ms to low 
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	
	StartTime = time.time()
	StopTime = time.time()
	
	# Save time of StartTime 
	while GPIO.input(GPIO_ECHO) == 0 : 
		StartTime = time.time()
				
		
	# Save time of arrival 
	while GPIO.input(GPIO_ECHO) == 1 : 
		StopTime = time.time()
	
		
	# Time difference between start and arrival
	TimeElapsed = StopTime - StartTime 
	
	# Multiply with the sonic speed (34300 cm/s)
	# And divided by 2, because sent and back 
	distance = (TimeElapsed * 34300) / 2
	
	return distance
	
if __name__ == '__main__' : 
	try : 
		
		while True : 
			dist = distance()
			print ("Measured Distance = %0.2f cm, %0.2fm" %(dist, dist/100))
			time.sleep(0.5)
			
	# Reset by Prising CTRL + C
	except KeyboardInterrupt : 
		print("Measurment stopped by the user")
		GPIO.cleanup()
