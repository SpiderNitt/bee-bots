import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(2, GPIO.OUT)            #to A0 of arduino
GPIO.setup(3, GPIO.OUT)	           #to A1 of arduino
while 1:
  GPIO.output(2, GPIO.HIGH)         #forward
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)
  GPIO.output(2, GPIO.HIGH)         #left 
  GPIO.output(3, GPIO.LOW)
  time.sleep(5)
  GPIO.output(2, GPIO.LOW)          #right
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)
  GPIO.output(2, GPIO.LOW)          #stop 
  GPIO.output(3, GPIO.LOW)
  time.sleep(5)
