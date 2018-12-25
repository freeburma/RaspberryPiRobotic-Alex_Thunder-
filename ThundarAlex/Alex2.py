import RPi.GPIO as gpio
import time 

'''
Moving Direction Diagram
	/\           /\
    7  ========= 13 
    11 ========= 15
    \/           \/  

'''
IN_1 = 7
IN_2 = 11
IN_3 = 13
IN_4 = 15

def Setup():
	# Setting up the GPIO output
	gpio.setmode(gpio.BOARD)
	gpio.setup(IN_1, gpio.OUT) 
	gpio.setup(IN_2, gpio.OUT) 
	gpio.setup(IN_3, gpio.OUT) 
	gpio.setup(IN_4, gpio.OUT) 
	
def Stop(): 
	gpio.output(IN_1, False)
	gpio.output(IN_2, False)
	gpio.output(IN_3, False)
	gpio.output(IN_4, False)
		
	
	
def GoForward():
	# Going forward 
	print("Going forward")
	gpio.output(IN_1, True)
	gpio.output(IN_4, True)
	time.sleep(3)

	gpio.output(IN_1, False)
	gpio.output(IN_4, False)
	time.sleep(1)

def GoBackward():
	# Going Backward  
	print("Going Backward")

	gpio.output(IN_2, True)
	gpio.output(IN_3, True)
	time.sleep(3)

	gpio.output(IN_2, False)
	gpio.output(IN_3, False)
	time.sleep(1)


'''
Moving Direction Diagram
	/\           /\
    7  ========= 13 
    11 ========= 15
    \/           \/  

'''
def TurnLeft():
	# Turn Left 
	print("Turn Left")
	gpio.output(IN_2, True)
	gpio.output(IN_4, True)
	time.sleep(3)

	gpio.output(IN_2, False)
	gpio.output(IN_4, False)
	time.sleep(1)




def TurnRight(): 
	# Turn Right 
	print("Turn Right")
	gpio.output(IN_1, True)
	gpio.output(IN_3, True)
	time.sleep(3)

	gpio.output(IN_1, False)
	gpio.output(IN_3, False)

def CleanUp():
	# Cleaning the gpio 
	gpio.cleanup()
	
	
if __name__ == "__main__": 
	
	print("[+] Program start ")
	
	Setup()
	Stop() # Set GPIO pins to false to use in another process
	GoForward()
	GoBackward()
	TurnRight()
	TurnLeft()
	
	Stop() # Set GPIO pins to false to use in another process

	
	print("Program finished ...")
	
	# Cleaning GPIO
	CleanUp()


