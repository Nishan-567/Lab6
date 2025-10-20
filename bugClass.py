#import 
import time
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
serialPin, latchPin, clockPin = 23, 24, 25
#import shifter
from shifter import Shifter

#instantiate a Shifter object
shifter = Shifter(serialPin, latchPin, clockPin)

class Bug:
	def __init__(self, shifter, timeStep=.1, x=3, isWrapOn=False):
		self.shifter = shifter
		self.timeStep = timeStep
		self.x = x
		self.isWrapOn = isWrapOn
		
		self.isRunning = False

	def start(self):
		#start LED motion
		self.isRunning = True
		try:
			while self.isRunning:
				pattern = 1 << self.x
				self.shifter.shiftByte(pattern) #light x LED
				time.sleep(self.timeStep) # sleep for timeStep
				
				#move left or right
				step = random.choice([-1, 1])
				self.x += step
				
				#check for wrapping
				if self.isWrapOn:
					#wrap 0 to 7 and 7 to 0
					self.x %= 8
				else:
					if self.x < 0:
						self.x = 0
					elif self.x > 7:
						self.x =7
		except KeyboardInterrupt:
			pass
		finally:
			self.stop()
			
	def stop(self):
		self.isRunning = False
		self.shifter.shiftByte(0) # turn off led
		GPIO.cleanup()










