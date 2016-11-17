import numpy as np
import time

from utils.fetchCube import fetchCube
from utils.goHome import goHome
from utils.moveFromHomeToRoom import moveFromHomeToRoom
from utils.scan360 import scan360toRoom
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

		# State machine steps:
		#  0 - scanning 360 for a room
		#  1 - moving into that room
		#  2 - search for and fetch the cube
		#  3 - deliver cube to the respective base
		self.state = 0
		self.roomQueue = ['b', 'a', 'c']

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
				print self.sensors[4], self.sensors[5], '\t', self.sensors[2]
				#print self.IO.getInputs()

				self.updateFSM()

				self.update()

	def updateFSM(self):

		if self.state == 0:

			#  0 - scanning 360 for a room

			scan360toRoom(self, self.roomQueue[0])

			if self.scan360_done:
				del self.scan360_done
				self.state += 1

		elif self.state == 1:

			#  1 - moving into that room

			moveFromHomeToRoom(self, self.roomQueue[0])

			if self.moveFromHomeToRoom_done:
				del self.moveFromHomeToRoom_done
				self.state += 1

		elif self.state == 2:

			#  2 - search for and fetch the cube

			fetchCube(self, self.roomQueue[0])

			if self.fetchCube_done:
				del self.fetchCube_done
				self.state += 1

		elif self.state == 3:

			#  3 - deliver cube to the respective base
			print '3 - deliver cube to the respective base'

			self.routine6()

			if self.routine6_done:
				self.state += 1

		elif self.state == 4:

			#  4 - go home
			print '4 - go home'

			goHome(self, self.roomQueue[0])

			if self.goHome_done:
				del self.goHome_done
				self.state = 0

	def onBase(self):
		return self.baseDetector.left.triggered() and self.baseDetector.right.triggered()

	def ObstacleToTheRight(self):
		return self.sensors[0] > IR_THRESHOLD
	def ObstacleToTheLeft(self):
		return self.sensors[1] > IR_THRESHOLD

	def routine6(self):
		self.routine6_done = False

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
				time.sleep(1)
				self.motors.stop()
				# remove this room from queue
				self.roomQueue.pop(0)
				self.routine6_done = True
			else:
				self.motors.moveForward()

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
