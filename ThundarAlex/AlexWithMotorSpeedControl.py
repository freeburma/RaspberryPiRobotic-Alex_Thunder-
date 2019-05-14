import RPi.GPIO as GPIO          
import time

# Working code -- Have to use BCM Board type to control motor
DutyCycle = 65
GPIO.setmode(GPIO.BCM)

# ================ Ultrasonic Sensor Port ================ 
GPIO_TRIGGER = 23 	# 16
GPIO_ECHO = 24 		# 18

# Ultrasonic Sensor
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
# ================ Ultrasonic Sensor Port ================ 


# ============== Line Tracking Sensor Port =============== 
D1 = 26 # 37
D2 = 19 # 35
D3 = 13 # 33
D4 = 6  # 31

GPIO.setup(D1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(D2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(D3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(D4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# ============== Line Tracking Sensor Port =============== 

# ====================== Motors Port ====================== 
# Motor
in1 = 4     # Pin 7 
in2 = 17	# Pin 11
en = 27		# Pin 13

in3 = 22    # Pin 15 
in4 = 10	# Pin 19
en2 = 9		# Pin 31

# First Motor
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

# Second Motor
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p=GPIO.PWM(en,1000)
p2=GPIO.PWM(en2,1000)


p.start(DutyCycle)
p2.start(DutyCycle)
# ====================== Motors Port ====================== 


def Distance(): 
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
	
def Left_LineTracking(): 
	
	
	if GPIO.input(D1) == GPIO.LOW : 
		# print("[!] Left (D1): White")
		return False	
	else : 
		# print("[-] D1: BLackkkk Line Found ...")
		return True	
		
def Right_LineTracking(): 
	
	
	if GPIO.input(D2) == GPIO.LOW : 
		# print("[@] (Right) D2: White ...")
		return False
	else : 
		# print("[-] D2: BLackkkk Line Found ...")
		return True		
		

def MotorWithSpeedControl():
	
	temp1=1
	
	
	print("\n")
	print("The default speed & direction of motor is LOW & Forward.....")
	print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
	print("\n")    

	while(1):

		x = raw_input()
		
		if x=='r':
			print("run")
			if(temp1==1):
				# Motor 1 
				GPIO.output(in1,GPIO.HIGH)
				GPIO.output(in2,GPIO.LOW)

				# Motor 2
				GPIO.output(in3,GPIO.HIGH)
				GPIO.output(in4,GPIO.LOW)

				print("forward")
				x='z'
			else:
				# Motor 1 
				GPIO.output(in1,GPIO.LOW)
				GPIO.output(in2,GPIO.HIGH)

				# Motor 3 
				GPIO.output(in3,GPIO.LOW)
				GPIO.output(in4,GPIO.HIGH)

				print("backward")
				x='z'


		elif x=='s':
			print("stop")
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.LOW)
			GPIO.output(in3,GPIO.LOW)
			GPIO.output(in4,GPIO.LOW)
			x='z'

		elif x=='f':
			print("forward")
			# Motor 1 
			GPIO.output(in1,GPIO.HIGH)
			GPIO.output(in2,GPIO.LOW)

			# Motor 2
			GPIO.output(in3,GPIO.HIGH)
			GPIO.output(in4,GPIO.LOW)
			temp1=1
			x='z'

		elif x=='b':
			print("backward")
			# Motor 1 
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)

			# Motor 3 
			GPIO.output(in3,GPIO.LOW)
			GPIO.output(in4,GPIO.HIGH)
			temp1=0
			x='z'

		elif x=='l':
			print("low")
			p.ChangeDutyCycle(25)
			p2.ChangeDutyCycle(25)
			x='z'

		elif x=='m':
			print("medium")
			p.ChangeDutyCycle(50)
			p2.ChangeDutyCycle(50)
			x='z'

		elif x=='h':
			print("high")
			p.ChangeDutyCycle(75)
			p2.ChangeDutyCycle(75)
			x='z'
		
		elif x=='xh':
			print("hightest")
			p.ChangeDutyCycle(100)
			p2.ChangeDutyCycle(100)
			x='z'    
			
		 
		
		elif x=='e':
			# GPIO.cleanup()
			break
		
		else:
			print("<<<  wrong data  >>>")
			print("please enter the defined data to continue.....")
			
def Forward(cusDuty): 
	print("forward")
	# Motor 1 
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)

	# Motor 2
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	
	p.ChangeDutyCycle(cusDuty)
	p2.ChangeDutyCycle(cusDuty)
	
	
	
def Backward(): 
	print("backward")
	# Motor 1 
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)

	# Motor 3 
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)	
	
	p.ChangeDutyCycle(DutyCycle)
	p2.ChangeDutyCycle(DutyCycle)
	
	

def GoRight(): 
	print("Right")
	# Motor 1 
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)

	# Motor 2
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	
	p.ChangeDutyCycle(DutyCycle)
	p2.ChangeDutyCycle(DutyCycle)
	
	
def GoLeft(): 
	print("Left")
	# Motor 1 
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)

	# Motor 2
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	
	p.ChangeDutyCycle(DutyCycle)
	p2.ChangeDutyCycle(DutyCycle)
	
def StopMortors(): 
	print("All motors stop")
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)
        
if __name__ == '__main__' : 

	print("Enter input: Press [q: to quit]")
	input_str = raw_input() ### Python 3 keyboard input

	while(input_str != 'q'): 
		# Reading keyboard input 
		input_str = raw_input() ### Python 3 keyboard input
		print(">>>>>>" + input_str)
		
		if input_str =='\x1b[A':
			print("Go Straight")
			Forward(80)

		elif input_str =='\x1b[B':
			print("Go Backward")
			Backward()

		elif input_str =='\x1b[C':
			print("Go right")
			GoRight()

		elif input_str =='\x1b[D':
			print("Go left")
			GoLeft()

		elif input_str == '0':
			print("StoPPPPPPPPPPP")
			StopMortors()
		
		elif input_str == 'q':
			break

		else: 
			print("Manual Mode")


	try : 
		
		'''
		# Testing 
		MotorWithSpeedControl()
				
		Forward()		
		time.sleep(6)
		
		Backward()		
		time.sleep(3)
		'''
		
		StopMortors() # Initializing 
		
		'''
		while True : 
			dist = Distance()
			print ("Measured Distance = %0.2f cm, %0.2fm" %(dist, dist/100))
			
			# An object detected 
			if (dist <= 3): 
				print("OOOOOOOO! Object Detected")
				StopMortors()	
			else:
			
				# Line Tracking
				left = Left_LineTracking()
				right = Right_LineTracking()
				
				# Go Left
				if (left == True and right == False) : 
					print ("<<<<<<<<<<<<<<<< Go Left")
					GoLeft()
						
					
				# Go Right	
				elif (left == False and right == True) : 
					print ("Go Right >>>>>>>>>>>>>>>>")
					GoRight()
					
				# Go straight	
				elif (left and right): 
					print (">>>>>>>>>> Straight <<<<<<<<<<")	
					Forward(100)
					
					
				else: 
					# StopMortors()	
					
					print (">>>>>>>>>> Straight with Object detection <<<<<<<<<<")	
					Forward(70)
					
										
					# An object detected 
					if (dist <= 3): 
						print("OOOOOOOO! Object Detected")
						StopMortors()	
					
					elif (dist >= 4 and dist <= 10): 
						print("Speed 66")
						Forward(66)	
						
					elif (dist >= 11 and dist <= 20): 
						print("Speed 68")
						Forward(68)		
						
					elif (dist >= 21 and dist <= 30): 
						print("Speed 69")
						Forward(69)	
						
					elif (dist >= 31 and dist <= 200): 
						print("Full Speed")
						Forward(100)

						
					else:
						print("OOOOOOOO! Object Detected")
						StopMortors()		
						
				
				
			
			time.sleep(0.5)
		GPIO.CleanUp()
		'''
		

	# Reset by Pressing CTRL + C
	except KeyboardInterrupt : 
		print("Measurement stopped by the user")
		GPIO.cleanup()        
