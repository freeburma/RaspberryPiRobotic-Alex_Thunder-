import RPi.GPIO as GPIO
import time
import datetime as dt

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
LIGHT_PIN = 20 # 2
GPIO.setup(LIGHT_PIN, GPIO.IN)


while True:
  print("Time: ", dt.datetime.now().strftime('%H:%M:%S'), GPIO.input(LIGHT_PIN))
  time.sleep(0.5)
  
