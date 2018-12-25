import RPi.GPIO as GPIO
import time 

# Preparing for line tracking sensor
TrackPin = 40
LedPin = 12

# Preparing for Motor Controller
Forward = 7
Backward = 11

TurnRight = 13
TurnLeft = 15 

def setup(): 
	# Setting up the GPIO Board
	GPIO.setmode(GPIO.BOARD)
	
	# Line Tracking Sensor 
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.setup(TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.HIGH)
	
	# Motor 
	GPIO.setup(Forward, GPIO.OUT)
	GPIO.setup(Backward, GPIO.OUT)
	GPIO.setup(TurnRight, GPIO.OUT)
	GPIO.setup(TurnLeft, GPIO.OUT)
	
def loop():
	
	# Infinate Loop
	while True: 
		if GPIO.input(TrackPin) == GPIO.LOW:
			print("[+] White")
			GPIO.output(LedPin, GPIO.HIGH) 
			
			GPIO.output(Forward, False)
		else: 
			print("[-] Black - Line found")
			GPIO.output(LedPin, GPIO.HIGH)
			
			# Going forward 
			GPIO.output(Forward, True)
			
def destroy(): 
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()
	
if __name__ == '__main__': 
	setup()
	
	try: 
		loop()
		
	except KeyboardInterrupt: 
		destroy()
