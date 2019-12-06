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

# ============== Obsticle Tracking Sensor Port =============== 
D3 = 13 # 33 - Right
D4 = 21  # 6 = 31 - Left GPIO: 5,6 to 11 is broken. Need to resolder

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
		
def Left_ObstecleTracking(): 
		
	if GPIO.input(D3) == GPIO.LOW : 
		# print("[-] D3: Object found on Left side ...")
		return True		
	else : 
		# print("[!] Left (D3): Object detected on Left side")
		return False
		
def Right_ObstecleTracking(): 
		
	if GPIO.input(D4) == GPIO.LOW : 
		# print("[-] D4: Object found on Right side ...")
		return True		
	else : 
		print("[!] Left (D4): Object NOTTTTT detected on Right side")
		return False				
		

			
def Forward(cusDuty): 
	# print("forward")
	# Motor 1 
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	
	p.ChangeDutyCycle(cusDuty)
	
	
	
	
def Backward(cusDuty): 
	# print("backward")
	# Motor 1 
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	
	p.ChangeDutyCycle(cusDuty)
	
	

def WheelStraight(): 
	# print("WheelStraight")
	
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

def GoRight(cusDuty): 
	# print("Right")
	
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	
	
	p2.ChangeDutyCycle(cusDuty)
	
	
def GoLeft(cusDuty): 
	# print("Left")
	
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
		
	p2.ChangeDutyCycle(cusDuty)
	
	
def Go_Forward_Left(custDutyTurn, custDutyMotor): 
	print("[/|\ <-] Go Backward and Left")
	## Go Left
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
		
	p2.ChangeDutyCycle(custDutyTurn)
	
	# Forward
	# Motor 1 
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	
	p.ChangeDutyCycle(custDutyMotor)
	
def Go_Forward_Right(custDutyTurn, custDutyMotor): 
	print("[/|\ ->] Go Backward and Right")
	## Go Right
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
		
	p2.ChangeDutyCycle(custDutyTurn)
	
	# Forward
	# Motor 1 
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	
	p.ChangeDutyCycle(custDutyMotor)
	
def Go_Backward_Left(custDutyTurn, custDutyMotor): 
	
	print("[\|/ <-] Go Backward and Left")
	''''''
	## Go Left
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
		
	p2.ChangeDutyCycle(custDutyTurn)
	
	## Backward
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	
	p.ChangeDutyCycle(custDutyMotor)
	''''''
	
def Go_Backward_Right(custDutyTurn, custDutyMotor): 
	print("[\|/ ->] Go Backward and Right")
	''''''
	## Go Right
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
		
	p2.ChangeDutyCycle(custDutyTurn)
	
	## Backward
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	
	p.ChangeDutyCycle(custDutyMotor)
	
def Go_Forward_Straight(custDutyTurn, custDutyMotor): 
	
	print("[/|\ /|\] Go Forward and Straight")
	## Wheel Straight
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)
	
	# Forward
	# Motor 1 
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	
def Go_Backward_Straight(custDutyTurn, custDutyMotor): 
	
	print("[\|/ /|\] Go Backward and Straight")
	## Wheel Straight
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)
	
	## Backward
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
		
	
def StopMortors(): 
	print("All motors stop")
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)
        
if __name__ == '__main__' : 
	
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
		print("o: Obstacle Avoidance Hello \r\n")
		print("l:  line trakcing \r\n")
		
		input_str = raw_input() ### Python 3 keyboard input
		
		while True : 
			
			
			
			# isBarrier = ObsticalAvoidance()
			isBarrierLeft = Left_ObstecleTracking()
			isBarrierRight = Right_ObstecleTracking()
			
			dist = Distance()
			
			
				
			
			print ("Measured Distance = %0.2f cm, %0.2fm" %(dist, dist/100))
			
			
			'''
			# An object detected 
			# if (dist <= 10 and isBarrier): 
			# if (dist <= 10 or isBarrier): 
			if (dist <= 10 or (isBarrierLeft and isBarrierRight)): 
				print("Main: OOOOOOOO! Object Detected")
				# StopMortors()	
				
				Backward(100)		
				time.sleep(0.3)
				
				## Action to turn
				Go_Backward_Left(turnSpeed, 100)
				time.sleep(0.3)
				
				
				
			else:
			'''
			
			## ==================================================================
			### Line Tracking Choose
			if input_str == "l":
				print("Line >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
				## ==================== Line Tracking Sensor Input ====================
				left = Left_LineTracking()
				right = Right_LineTracking()

				if (dist < 20):
    				
					motorSpeed = 100
					if (isBarrierLeft and (not isBarrierRight)):
						
						Go_Backward_Left(turnSpeed, motorSpeed)
						time.sleep(2)
						
					if ((not isBarrierLeft) and isBarrierRight): 
						
						Go_Backward_Right(turnSpeed, motorSpeed)
						time.sleep(2)
						
					if (isBarrierLeft and isBarrierRight): 
						Go_Backward_Straight(turnSpeed, motorSpeed)
						time.sleep(1.5)

				else: 						
				
					motorSpeed = 50
					if (left and (not right)):
								
						Go_Forward_Left(turnSpeed, motorSpeed)
							
					elif ((not left) and right): 
						
						Go_Forward_Right(turnSpeed, motorSpeed)


					elif ((not left) and (not right)): 
						print("[-] No line found")
						StopMortors()

					else: 
						Go_Forward_Straight(turnSpeed, motorSpeed)
			
			## ==================================================================	
			## ==================== Object Detection Chocice ====================	
			if input_str == "o":
				
				''''''
				print (">>>>>>>>>> Straight with Object detection <<<<<<<<<<")	
				#Forward(70)
				
									
				# An object detected 
				
				# if (dist <= 10 and isBarrierLeft and isBarrierRight):
				if (dist < 20):
					
					'''
					motorSpeed = 100
					Go_Backward_Straight(turnSpeed, motorSpeed)
					time.sleep(2)
					
					'''
					if (isBarrierLeft and (not isBarrierRight)):
						StopMortors()
						time.sleep(0.1)

						
						motorSpeed = 100
						
						Go_Backward_Left(turnSpeed, motorSpeed)
						time.sleep(1.5)
						
					if ((not isBarrierLeft) and isBarrierRight): 
						StopMortors()
						time.sleep(0.1)

						
						motorSpeed = 100
						
						Go_Backward_Right(turnSpeed, motorSpeed)
						time.sleep(1.5)
						
					if (isBarrierLeft and isBarrierRight): 
						
						StopMortors()
						time.sleep(0.1)

						motorSpeed = 100
						Go_Backward_Straight(turnSpeed, motorSpeed)
						time.sleep(1.2)
					
					
				elif (dist >= 21 and dist <= 30): 
					
					
					motorSpeed = 35
					
					if (isBarrierLeft and (not isBarrierRight)):
						# print("LEFFFFFFFFFFFFFFFFFFFF_T")
						Go_Forward_Right(turnSpeed, motorSpeed)
						
					elif ((not isBarrierLeft) and isBarrierRight): 
						# print("RIGGGGGGGGGGGGGGGGGGGGG_T")
						Go_Forward_Left(turnSpeed, motorSpeed)
						
					else: 
						Go_Forward_Straight(turnSpeed, motorSpeed)
						
				elif (dist >= 31 and dist <= 40): 
					
					
					motorSpeed = 45
					
					if (isBarrierLeft and (not isBarrierRight)):
						# print("LEFFFFFFFFFFFFFFFFFFFF_T")
						Go_Forward_Right(turnSpeed, motorSpeed)
						
					elif ((not isBarrierLeft) and isBarrierRight): 
						# print("RIGGGGGGGGGGGGGGGGGGGGG_T")
						Go_Forward_Left(turnSpeed, motorSpeed)
						
					else: 
						Go_Forward_Straight(turnSpeed, motorSpeed)
						
				elif (dist >= 41 and dist <= 60): 
					
					
					motorSpeed = 55
					
					if (isBarrierLeft and (not isBarrierRight)):
						# print("LEFFFFFFFFFFFFFFFFFFFF_T")
						Go_Forward_Right(turnSpeed, motorSpeed)
						
					elif ((not isBarrierLeft) and isBarrierRight): 
						# print("RIGGGGGGGGGGGGGGGGGGGGG_T")
						Go_Forward_Left(turnSpeed, motorSpeed)
						
					else: 
						Go_Forward_Straight(turnSpeed, motorSpeed)
					
				elif (dist >= 60 and dist <= 150): 
					
					motorSpeed = 100
					
					if (isBarrierLeft and (not isBarrierRight)):
						# print("LEFFFFFFFFFFFFFFFFFFFF_T")
						Go_Forward_Right(turnSpeed, motorSpeed)
						
					elif ((not isBarrierLeft) and isBarrierRight): 
						# print("RIGGGGGGGGGGGGGGGGGGGGG_T")
						Go_Forward_Left(turnSpeed, motorSpeed)
						
					else: 
						Go_Forward_Straight(turnSpeed, motorSpeed)

										
				else:
					
					motorSpeed = 100
					
					if (isBarrierLeft and (not isBarrierRight)):
						# print("LEFFFFFFFFFFFFFFFFFFFF_T")
						Go_Forward_Right(turnSpeed, motorSpeed)
						
					elif ((not isBarrierLeft) and isBarrierRight): 
						# print("RIGGGGGGGGGGGGGGGGGGGGG_T")
						Go_Forward_Left(turnSpeed, motorSpeed)
						
					else: 
						Go_Forward_Straight(turnSpeed, motorSpeed)
					
					
					
					
					
					
			
					
			
			time.sleep(0.25)
		GPIO.CleanUp()
		
		''' '''
		

	# Reset by Pressing CTRL + C
	except KeyboardInterrupt : 
		print("Measurement stopped by the user")
		GPIO.cleanup()        
