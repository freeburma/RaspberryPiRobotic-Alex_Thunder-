import RPi.GPIO as GPIO          
from time import sleep


# Working code -- Have to use BCM Board type 

in1 = 4    # Pin 7 
in2 = 17	# Pin 11
en = 27		# Pin 13

in3 = 22    # Pin 7 
in4 = 10	# Pin 11
en2 = 9		# Pin 13

temp1=1

GPIO.setmode(GPIO.BCM)

# First Motor
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

# Second Motor
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2,1000)


p.start(25)
p2.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):

    x=raw_input()
    
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
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
