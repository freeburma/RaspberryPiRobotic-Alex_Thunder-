import RPi.GPIO as GPIO
import time 

'''
Multiple Line Tracking Sensor with 4 inputs 

'''


# Set GPIO Pins 
D1 = 37
D2 = 35
D3 = 33
D4 = 31

def setup(): 
	
	GPIO.setmode(GPIO.BOARD)
	# Set GPIO directin (IN / OUT)
	GPIO.setup(D1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(D2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(D3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(D4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	

def tracking(): 
	if GPIO.input(D1) == GPIO.LOW : 
		print("[!] D1: White")
	else : 
		print("[-] D1: BLackkkk Line Found ...")
		
	if GPIO.input(D2) == GPIO.LOW : 
		print("[@] D2: White ...")
	else : 
		print("[-] D2: BLackkkk Line Found ...")
		
	if GPIO.input(D3) == GPIO.LOW : 
		print("[*] D3: White")
	else : 
		print("[-] D3: BLackkkk Line Found ...")
		
	if GPIO.input(D4) == GPIO.LOW : 
		print("[&] D4: White")
	else : 
		print("[-] D4: BLackkkk Line Found ...")		
	
	
	
if __name__ == '__main__' : 
	try : 
		setup()
		
		while True : 
			tracking()
			time.sleep(0.5)
			
	# Reset by Prising CTRL + C
	except KeyboardInterrupt : 
		print("Measurment stopped by the user")
		GPIO.cleanup()
