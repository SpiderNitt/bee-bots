
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(2, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(3, GPIO.OUT)  
while 1:
  GPIO.output(2, GPIO.HIGH)         # set GPIO24 to 1/GPIO.HIGH/True  
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)
  GPIO.output(2, GPIO.HIGH)         # set GPIO24 to 1/GPIO.HIGH/True  
  GPIO.output(3, GPIO.LOW)
  time.sleep(5)
  GPIO.output(2, GPIO.LOW)         # set GPIO24 to 1/GPIO.HIGH/True  
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)
  GPIO.output(2, GPIO.LOW)         # set GPIO24 to 1/GPIO.HIGH/True  
  GPIO.output(3, GPIO.LOW)
  time.sleep(5)
