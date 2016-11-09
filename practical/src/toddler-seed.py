import numpy as np
import time

from vision.visionUtils import *
from settings import *

from baseDetector import BaseDetector
from gripper import Gripper
from hallCounter import HallCounter
from whiskers import Whiskers

# Main Toddler class
class Toddler:
	# Initialiser
	def __init__(self, IO):
		# Store the instance of IO for later
		self.IO = IO

		self.baseDetector = BaseDetector(self.IO)
		self.gripper = Gripper(self.IO)
		self.hallCounter = HallCounter(self.IO)
		self.whiskers = Whiskers(self.IO)
		self.visionUtils = VisionUtils(self.IO)

		self.resetTurnSleep()

	def resetTurnSleep(self):
		# 0 - none, 1 - just turned left, 2 - just turned right
		self.turnAux = 0
		self.initHallCount = 0
		self.turnSleep = 0
	def incAndSleep(self):
		if self.initHallCount == 0:
			self.initHallCount = self.hallCounter.getCount()
		self.turnSleep += 0.2
		time.sleep(self.turnSleep)
		print 'Incremented turnSleep to ', self.turnSleep

	# This is a callback that will be called repeatedly.
	# It has its dedicated thread so you can keep blocking it.
	def Control(self, OK):
		while OK():
			self.sensors = self.IO.getSensors()
			#print self.sensors

			if self.gripper.sensesCube():
				self.gripper.close()
			else:
				self.gripper.open()

			if self.onBase():
				#print '- ON BASE -'
				self.gripper.open()

			#print
			#print self.lastInputs

			#if self.whiskers.left.triggered() or self.whiskers.right.triggered():
			#	print self.whiskers
			#else:
			#	print self.inputs

			if self.ObstacleToTheRight():
				self.TurnLeft()

				if self.turnAux == 2:
					self.incAndSleep()
				self.turnAux = 1
			elif self.ObstacleToTheLeft():
				self.TurnRight()

				if self.turnAux == 1:
					self.incAndSleep()
				self.turnAux = 2
			else:
				if self.turnSleep > 0:
					if self.hallCounter.getCount() - self.initHallCount > 2:
						self.resetTurnSleep()

				self.MoveForward()

			self.update()

	def update(self):
		self.gripper.update()

	def onBase(self):
		return self.baseDetector.left.triggered() and self.baseDetector.right.triggered()

	def ObstacleToTheRight(self):
		return self.sensors[0] > IR_THRESHOLD
	def ObstacleToTheLeft(self):
		return self.sensors[1] > IR_THRESHOLD

	def STOP(self):
		self.IO.setMotors(0, 0)

	def MoveBackwards(self):
		self.IO.setMotors(-MOTOR_MAX_SPEED, -MOTOR_MAX_SPEED)
	def MoveForward(self):
		self.IO.setMotors(MOTOR_MAX_SPEED, MOTOR_MAX_SPEED)

	def EvadeLeft(self):
		self.IO.setMotors(-MOTOR_MAX_SPEED, -MOTOR_LOW_SPEED)
	def EvadeRight(self):
		self.IO.setMotors(-MOTOR_LOW_SPEED, -MOTOR_MAX_SPEED)

	def TurnLeft(self):
		self.IO.setMotors(MOTOR_MED_SPEED, -MOTOR_MED_SPEED)
	def TurnRight(self):
		self.IO.setMotors(-MOTOR_MED_SPEED, MOTOR_MED_SPEED)

	# This is a callback that will be called repeatedly.
	# It has its dedicated thread so you can keep blocking it.
	def Vision(self, OK):
		if (USE_VISION):
			# Set the camera resolution
			self.IO.cameraSetResolution('medium')

			while OK():
				# Grab the image
				self.IO.cameraGrab()

				# Read the image
				cameraImage = self.IO.cameraRead()
				#self.IO.imshow('Camera', cameraImage)

				# Process camera input
				self.visionUtils.process(cameraImage)

				# Dump next couple of frames...
				for i in range(0, 10):
					self.IO.cameraGrab()

### eof ###
