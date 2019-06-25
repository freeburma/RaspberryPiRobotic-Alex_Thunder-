import RPi.GPIO as GPIO          
import time, datetime
import random

# Working code -- Have to use BCM Board type to control motor
DutyCycle = 65
GPIO.setmode(GPIO.BCM)

# ================ Obstical Avoidance Sensor Port =======
ObstaclePin = 20
GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ================ Obstical Avoidance Sensor Port =======



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

def ObsticalAvoidance(): 
	
	if (GPIO.input(ObstaclePin) == 0): ### Obstacle detected
		print(str(datetime.datetime.now().time()) + " >> Barrier is detected !")
		return True
	
	return False


def Distance(): 
	# Set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
	
	# Set Trigger after 0.01ms to low 
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	
	StartTime = time.time()
	StopTime = time.time()
	count = time.time()
	
	# Save time of StartTime 
	# while GPIO.input(GPIO_ECHO) == 0 : 
	while (GPIO.input(GPIO_ECHO) == 0) and (time.time() - count < 0.1): 
		StartTime = time.time()
	
	count = time.time()			
		
	# Save time of arrival 
	while (GPIO.input(GPIO_ECHO) == 1) and (time.time() - count < 0.1): 
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
		
'''
	Allows to test forward, backward, trun left and turn right by using keyboard, 
	however, you needs to press "Enter" key to perform. 
'''
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
	# GPIO.output(in3,GPIO.HIGH)
	# GPIO.output(in4,GPIO.LOW)
	
	p.ChangeDutyCycle(cusDuty)
	p2.ChangeDutyCycle(cusDuty)
	
	
	
def Backward(cusDuty): 
	print("backward")
	# Motor 1 
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	
	p.ChangeDutyCycle(cusDuty)
	
	

def WheelStriaght(): 
	print("WheelStriaght")
	
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

def GoRight(cusDuty): 
	print("Right")
	
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	
	
	p2.ChangeDutyCycle(cusDuty)
	
	
def GoLeft(cusDuty): 
	print("Left")
	
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
		
	p2.ChangeDutyCycle(cusDuty)
	
	
def Go_Forward_Left(custDutyTurn, custDutyMotor, restTime): 
	GoLeft(custDutyTurn)
	time.sleep(restTime)
	Forward(custDutyMotor)
	
def Go_Forward_Right(custDutyTurn, custDutyMotor, restTime): 
	GoRight(custDutyTurn)
	time.sleep(restTime)
	Forward(custDutyMotor)
	
def Go_Backward_Left(custDutyTurn, custDutyMotor, restTime, motorTime): 
	GoLeft(custDutyTurn)
	#time.sleep(restTime)
	Backward(custDutyMotor)
	time.sleep(motorTime)
	
def Go_Backward_Right(custDutyTurn, custDutyMotor, restTime, motorTime): 
	GoRight(custDutyTurn)
	time.sleep(restTime)
	Backward(custDutyMotor)		
	time.sleep(motorTime)
	
def Go_Forward_Straight(custDutyTurn, custDutyMotor): 
	WheelStriaght()
	Forward(custDutyMotor)	
	
def Go_Backward_Straight(custDutyTurn, custDutyMotor): 
	WheelStriaght()
	Backward(custDutyMotor)
		
	
def StopMortors(): 
	print("All motors stop")
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)
        
if __name__ == '__main__' : 
	
	'''

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
			
	'''


	try : 
		
		restTime = 0.60
		turnSpeed = 100
		motorSpeed = 60
		lineTracking = True
		
		StopMortors() # Initializing 
		''' 
		# Testing 
		# MotorWithSpeedControl()
				
		Forward(100)		
		time.sleep(3)
		
		Backward(100)		
		time.sleep(3)	
		
		GoRight(100)
		time.sleep(3)
		
		
		
		GoLeft(100)
		time.sleep(3)
				
		
		''' 
		
		
		
		''' '''
		print("Enter Input \r\n")
		print("o: Obstacle Avoidance \r\n")
		print("l:  line trakcing \r\n")
		
		input_str = raw_input() ### Python 3 keyboard input
		
		while True : 
			
			
			
			isBarrier = ObsticalAvoidance()
			
			dist = Distance()
			
			
				
			
			print ("Measured Distance = %0.2f cm, %0.2fm" %(dist, dist/100))
			
			# An object detected 
			# if (dist <= 10 and isBarrier): 
			if (dist <= 10 or isBarrier): 
				print("Main: OOOOOOOO! Object Detected")
				# StopMortors()	
				
				Backward(100)		
				time.sleep(0.3)
				
				# Action to turn
				Go_Backward_Left(turnSpeed, 100, 0.1, 1)
				
				
				'''
				randNum = random.randint(0, 2)
				
				if randNum == 0: 
					GoLeft(turnSpeed)	
					time.sleep(0.2)					
					Backward(motorSpeed)
					time.sleep(0.3)
					
					GoRight(turnSpeed)	
					time.sleep(0.2)					
					Backward(motorSpeed)
					time.sleep(0.3)
					
					# GoRight(turnSpeed)
					Go_Forward_Straight(turnSpeed, motorSpeed)					
					time.sleep(0.3)
					
				elif randNum == 1: 
					
					GoRight(turnSpeed)	
					time.sleep(0.2)					
					Backward(motorSpeed)
					time.sleep(0.5)
					
					GoLeft(turnSpeed)	
					time.sleep(0.2)				
					Backward(motorSpeed)
					time.sleep(0.5)
					
					# GoRight(turnSpeed)
					Go_Forward_Straight(turnSpeed, motorSpeed)					
					time.sleep(0.3)
				
				else: 
					GoRight(turnSpeed)	
					time.sleep(0.2)				
					Backward(motorSpeed)
					time.sleep(0.5)
					
					GoRight(turnSpeed)					
					Backward(motorSpeed)
					time.sleep(0.5)
					
					
					Go_Forward_Straight(turnSpeed, motorSpeed)					
					time.sleep(0.3)	
				'''
				
					
				
			else:
			
				### Line Tracking Choose
				if input_str == "l":
					
					# Line Tracking Sensor Input
					left = Left_LineTracking()
					right = Right_LineTracking()
					
					print (">>>>>>>>>>>>>>> Go Straight >>>>>>>>>>>>>>>>")
					Go_Forward_Straight(turnSpeed, motorSpeed)
					
					# Go Left
					if (left == True and right == False) : 
						print ("<<<<<<<<<<<<<<<< Go Left")						
						Go_Forward_Left(turnSpeed, motorSpeed, restTime)
							
						
					# Go Right	
					elif (left == False and right == True) : 
						print ("Go Right >>>>>>>>>>>>>>>>")
						Go_Forward_Right(turnSpeed, motorSpeed, restTime)
						time.sle
						
						
					# else: 
						# print (">>>>>>>>>>>>>>> Go Straight >>>>>>>>>>>>>>>>")
						Go_Forward_Straight(turnSpeed, motorSpeed)
					
						# print ("------------ SEARCHING for LINE -------------")	
						# Go_Backward_Straight(turnSpeed, 30)
					
					
				else: 
					
					print (">>>>>>>>>> Straight with Object detection <<<<<<<<<<")	
					Forward(70)
					
										
					# An object detected 
					if (dist <= 10 and isBarrier):
						print("Object Tracking: OOOOOOOO! Object Detected. ")
						# Backward(100)
						
						# GoLeft(100)
						StopMortors()
					
					# elif (dist >= 7 and dist <= 10): 
						# print("Speed 10")
						# Forward(10)	
						
					elif (dist >= 11 and dist <= 20): 
						print("Speed 20")
						Forward(20)		
						
					elif (dist >= 21 and dist <= 30): 
						print("Speed 35")
						Forward(35)	
						
					elif (dist >= 31 and dist <= 276): 
						print("Full Speed 85")
						Forward(85)

					
					else:
						print("Full Speed 100")
						Forward(100)	
					
				
				
			
			time.sleep(0.25)
		GPIO.CleanUp()
		
		''' '''
		

	# Reset by Pressing CTRL + C
	except KeyboardInterrupt : 
		print("Measurement stopped by the user")
		GPIO.cleanup()        
