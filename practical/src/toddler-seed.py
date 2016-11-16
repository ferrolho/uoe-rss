import numpy as np
import time

from utils.scan360 import do360scanToRoom
from vision.visionUtils import *
from settings import *

from baseDetector import BaseDetector
from gripper import Gripper
from hallCounter import HallCounter
from motors import Motors
from whiskers import Whiskers

# Main Toddler class
class Toddler:
	# Initialiser
	def __init__(self, IO):
		# Store the instance of IO for later
		self.IO = IO

		# 0 - looking for wall
		# 1 - turning to opening
		self.state = 0
		self.cubeHasBeenSeen = False

		if (USE_CONTROL):
			self.baseDetector = BaseDetector(self.IO)
			self.gripper = Gripper(self.IO)
			self.hallCounter = HallCounter(self.IO)
			self.motors = Motors(self.IO)
			self.whiskers = Whiskers(self.IO)

			self.resetTurnSleep()

		if (USE_VISION):
			self.visionUtils = VisionUtils(self.IO)

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
		if (USE_CONTROL):
			while OK():
				self.sensors = self.IO.getSensors()
				#print self.sensors
				#print self.IO.getInputs()

				#self.routine5()
				do360scanToRoom(self, 'c')

				self.update()

	def onBase(self):
		return self.baseDetector.left.triggered() and self.baseDetector.right.triggered()

	def ObstacleToTheRight(self):
		return self.sensors[0] > IR_THRESHOLD
	def ObstacleToTheLeft(self):
		return self.sensors[1] > IR_THRESHOLD

	def routine6(self):
		if self.ObstacleToTheRight():
			self.motors.turnLeftOnSpot()

			if self.turnAux == 2:
				self.incAndSleep()
			self.turnAux = 1
		elif self.ObstacleToTheLeft():
			self.motors.turnRightOnSpot()

			if self.turnAux == 1:
				self.incAndSleep()
			self.turnAux = 2
		else:
			if self.turnSleep > 0:
				if self.hallCounter.getCount() - self.initHallCount > 2:
					self.resetTurnSleep()

			if self.onBase():
				print '- ON BASE -'
				self.motors.stop()
				self.gripper.openNow()
				time.sleep(1)
				self.motors.moveBackwards()
				time.sleep(2)
				self.motors.stop()
				self.state += 1
			else:
				self.motors.moveForward()

	def routine5(self):
		if self.state == 2:
			self.motors.moveForward()
			if self.hallCounter.timerIsDone():
				self.motors.stop()
				self.state += 1
				if DEST_ROOM == 1:
					self.hallCounter.setTimer(4)
				elif DEST_ROOM == 2:
					self.hallCounter.setTimer(3)
		elif self.state == 3:
			if DEST_ROOM == 1:
				self.motors.turnLeft()
				if self.hallCounter.timerIsDone():
					self.motors.stop()
					self.state += 1
			elif DEST_ROOM == 2:
				self.motors.turnRight()
				if self.hallCounter.timerIsDone():
					self.motors.stop()
					self.state += 1
			elif DEST_ROOM == 3:
				self.motors.turnRight()
				time.sleep(0.2)
				self.motors.stop()
				self.state += 1
		elif self.state == 4:
			self.routine3()
		elif self.state == 5:
			self.routine6()

	def routine3(self):
		print 'routine3()'

		if self.gripper.sensesCube():
			self.gripper.close()
			self.motors.stop()
			print '- GOT DA CUBE -'
			self.state += 1

		if not self.gripper.isTransportingCube():
			if self.visionUtils.cubeRelativePos is not None:
				print 'Testing - %d' % self.visionUtils.cubeRelativePos
				self.cubeHasBeenSeen = True

				if self.visionUtils.cubeRelativePos == 1:
					print 'DONE'
					self.motors.moveForward()
					time.sleep(0.8)
				else:
					if self.visionUtils.cubeRelativePos == 0:
						print 'turnLeft'
						self.motors.turnLeft()
					elif self.visionUtils.cubeRelativePos == 2:
						print 'turnRight'
						self.motors.turnRight()

					time.sleep(0.1)

				self.motors.stop()
				self.waitForNewFrame()
			else:
				if self.cubeHasBeenSeen:
					self.motors.moveForward()
				else:
					self.motors.turnLeft()
					time.sleep(0.1)
					self.motors.stop()
					self.waitForNewFrame()

	def waitForNewFrame(self):
		lastFrameID = self.visionUtils.framesProcessed
		print 'Waiting for next frame'
		while (lastFrameID == self.visionUtils.framesProcessed):
			time.sleep(0.1)
		print 'New frame!'

	def routine2(self):
		if self.hallCounter.getCount() < 40:
			self.motors.moveForward()
		elif self.hallCounter.getCount() < 46:
			self.motors.turnRight()
		elif self.hallCounter.getCount() < 52:
			self.motors.turnLeft()
		else:
			self.motors.stop()

	def update(self):
		self.gripper.update()

	# This is a callback that will be called repeatedly.
	# It has its dedicated thread so you can keep blocking it.
	def Vision(self, OK):
		if (USE_VISION):
			# Set the camera resolution
			self.IO.cameraSetResolution('medium')

			#self.IO._cap.set(cv2.CAP_PROP_FPS, 15)
			#print self.IO._cap.get(cv2.CAP_PROP_FPS)

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
