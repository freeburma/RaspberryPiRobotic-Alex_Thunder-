import RPi.GPIO as GPIO
import datetime

ObstaclePin = 20

def setup(): 
	GPIO.setmode(GPIO.BCM) 
	GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
def loop(): 
	while True: 
		if (0 == GPIO.input(ObstaclePin)): 
			print(str(datetime.datetime.now().time()) + " >> Barrier is detected !")
			

def destroy(): 
	GPIO.cleanup()
	
	
if __name__ == '__main__': 
	setup()
	try: 
		loop()
	
	except KeyboardInterrupt: 
		destroy()


