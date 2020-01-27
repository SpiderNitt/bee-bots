
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(2, GPIO.OUT)            #to A0 of arduino
GPIO.setup(3, GPIO.OUT)	           #to A1 of arduino
GPIO.setup(4, GPIO.OUT)            #to reset of arduino . Default : HIGH ; pulled to ground when 					    reset required
while 1:
  GPIO.output(4, GPIO.LOW)         #forward
  time.sleep(0.3)
  GPIO.output(4, GPIO.HIGH)
  GPIO.output(2, GPIO.HIGH)         
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)

  GPIO.output(4, GPIO.LOW)         #left
  time.sleep(0.3)
  GPIO.output(4, GPIO.HIGH)
  GPIO.output(2, GPIO.HIGH)          
  GPIO.output(3, GPIO.LOW)
  time.sleep(5)
  
  GPIO.output(4, GPIO.LOW)          #right
  time.sleep(0.3)
  GPIO.output(4, GPIO.HIGH)
  GPIO.output(2, GPIO.LOW)          
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)
  
  GPIO.output(4, GPIO.LOW)	   #stop
  time.sleep(0.3)
  GPIO.output(4, GPIO.HIGH)
  GPIO.output(2, GPIO.LOW)         
  GPIO.output(3, GPIO.LOW)
  time.sleep(5)
