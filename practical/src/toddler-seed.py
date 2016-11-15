import numpy as np
import time

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
		self.minRight = 0

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

				self.routine3()

				self.update()

	def facingWall(self, left, right):
		WALL_DIST_THRESHOLD = 180
		return left > WALL_DIST_THRESHOLD and right > WALL_DIST_THRESHOLD

	def routine5(self):
		right, left = self.sensors[0], self.sensors[1]

		if self.state == 0:
			print '{} x {}'.format(left, right)
			self.motors.turnRightOnSpot()

			if self.facingWall(left, right):
				print '- FACING WALL -'
				self.state = 1
				self.minRight = right
		elif self.state == 1:
			print '{} x {}'.format(left, right)

			if right <= self.minRight:
				self.minRight = right
			elif left < 200:
				print '- FOUND OPENING -'
				self.motors.stop()
				time.sleep(0.1)

				self.state = 2
				self.hallCounter.setTimer(60)
		elif self.state == 2:
			self.motors.moveForward()
			if self.hallCounter.timerIsDone():
				self.motors.stop()
				self.state = 3
				self.hallCounter.setTimer(12)
		elif self.state == 3:
			self.motors.turnLeft()
			if self.hallCounter.timerIsDone():
				self.motors.stop()
				self.state = 4

	def routine3(self):
		if self.gripper.sensesCube():
			self.gripper.close()
			self.motors.stop()

		if not self.gripper.isTransportingCube():
			if self.visionUtils.centroid_x:
				print 'Testing - %d' % self.visionUtils.centroid_x

				# use dynamic thresholds for long-range scan
				if 100 <= self.visionUtils.centroid_x <= 170:
					print 'DONE'
					self.motors.moveForward()
				else:
					if self.visionUtils.centroid_x <= 100:
						print 'turnLeft'
						self.motors.turnLeft()
					elif self.visionUtils.centroid_x >= 170:
						print 'turnRight'
						self.motors.turnRight()

					time.sleep(0.1)
					self.motors.stop()

					lastFrameID = self.visionUtils.framesProcessed
					print 'Waiting for next frame'
					while (lastFrameID == self.visionUtils.framesProcessed):
						time.sleep(0.1)
					print 'New frame!'
			else:
				self.motors.stop()

	def routine2(self):
		if self.hallCounter.getCount() < 40:
			self.motors.moveForward()
		elif self.hallCounter.getCount() < 46:
			self.motors.turnRight()
		elif self.hallCounter.getCount() < 52:
			self.motors.turnLeft()
		else:
			self.motors.stop()

	def routine1(self):
		print 'Routine 1 running ...'

		if self.gripper.sensesCube():
			self.gripper.close()
		else:
			self.gripper.open()

		if self.onBase():
			#print '- ON BASE -'
			self.gripper.open()

		if self.ObstacleToTheRight():
			self.motors.turnLeft()

			if self.turnAux == 2:
				self.incAndSleep()
			self.turnAux = 1
		elif self.ObstacleToTheLeft():
			self.motors.turnRight()

			if self.turnAux == 1:
				self.incAndSleep()
			self.turnAux = 2
		else:
			if self.turnSleep > 0:
				if self.hallCounter.getCount() - self.initHallCount > 2:
					self.resetTurnSleep()

			self.motors.moveForward()

	def update(self):
		self.gripper.update()

	def onBase(self):
		return self.baseDetector.left.triggered() and self.baseDetector.right.triggered()

	def ObstacleToTheRight(self):
		return self.sensors[0] > IR_THRESHOLD
	def ObstacleToTheLeft(self):
		return self.sensors[1] > IR_THRESHOLD

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
