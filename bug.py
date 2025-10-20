import RPi.GPIO as GPIO
import time
from bugClass import Bug

GPIO.setmode(GPIO.BCM)

serialPin, latchPin, clockPin = 23, 24, 25
#import shifter
from shifter import Shifter

#instantiate a Shifter object
shifter = Shifter(serialPin, latchPin, clockPin)

#3 GPIO pins
s1,s2,s3 = 17,27,22

GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# initial bug with default parameters
bug = Bug(shifter, timeStep=.1, x=3, isWrapOn=False)

#track s2 val(wraping)
s2Previous = GPIO.input(s2)


try:
  while 1:
    s1_state = GPIO.input(s1)
    s2_state = GPIO.input(s2)
    s3_state = GPIO.input(s3)
    
    #check s1 to see if s1 hgh
    if s1_state == GPIO.HIGH:
      print("Bug started")
      bug.start()
    #stop if
    else:
      print("Bug Stopped")
      bug.stop()

    #check is s2_state changed
    if s2_state != s2Previous:
      bug.isWrapOn = not bug.isWarpOn #flip between true and false
      print(f"Wrap mode: {bug.isWrapOn}")
    s2Previous = s2_state

    #check s3 and increase speed
    if s3_state == GPIO.HIGH:
      bug.timeStep = .1/3
    else:
      bug.timeStep = .1

except KeyboardInterrupt:
  pass
