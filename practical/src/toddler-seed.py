#!/usr/bin/env python
__TODDLER_VERSION__ = "1.0.0"

import cv2
import numpy as np
import time

from baseDetector import *
from featureMatching import *
from gripper import Gripper
from random import randint
from resourceData import *
from sceneData import *
from settings import *
from whiskers import *


def InitResources(resources):
	for name in RESOURCE_NAMES:
		resources.append(ResourceData(name))


# Main Toddler class
class Toddler:
	# Initialiser
	def __init__(self, IO):
		# Store the instance of IO for later
		self.IO = IO

		self.baseDetector = BaseDetector(self.IO)
		self.gripper  =  Gripper(self.IO)
		self.whiskers = Whiskers(self.IO)

		# Add more initialisation code here
		self.hallCounter = 0

		self.resetTurnSleep()

		self.resetVisionFlags()

		self.resourcesData = []
		InitResources(self.resourcesData)


	def resetTurnSleep(self):
		# 0 - none, 1 - just turned left, 2 - just turned right
		self.turnAux = 0
		self.initHallCount = 0
		self.turnSleep = 0
	def incAndSleep(self):
		if self.initHallCount == 0:
			self.initHallCount = self.hallCounter
		self.turnSleep += 0.2
		time.sleep(self.turnSleep)
		print 'Incremented turnSleep to ', self.turnSleep

	def ResourceIsVisible(self):
		for visible in self.visibleResources:
			if visible:
				return True


	# This is a callback that will be called repeatedly.
	# It has its dedicated thread so you can keep blocking it.
	def Control(self, OK):
		while OK():
			if hasattr(self, 'inputs'):
				self.lastInputs = self.inputs
				self.inputs = list(self.IO.getInputs())
			else:
				self.inputs = list(self.IO.getInputs())
				self.lastInputs = self.inputs

			self.sensors = self.IO.getSensors()
			print self.sensors

			if self.GripperSensorTriggered():
				self.gripper.close()
			else:
				self.gripper.open()

			if self.onBase():
				print '- ON BASE -'

			#print
			#print self.lastInputs

			#if self.whiskers.left.triggered() or self.whiskers.right.triggered():
			#	print self.whiskers
			#else:
			#	print self.inputs

			if self.lastInputs[7] != self.inputs[7]:
				self.hallCounter += 1
			#print 'Travelled distance: %d' % self.hallCounter

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
					if self.hallCounter - self.initHallCount > 2:
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
	def GripperSensorTriggered(self):
		return self.sensors[3] < 40

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


	def ScanForCubeFarAway(self, rawCameraImage):
		height, width, channels = rawCameraImage.shape
		croppedCameraImage = rawCameraImage[0:height / 2, 0:width]

		hsv = cv2.cvtColor(croppedCameraImage, cv2.COLOR_BGR2HSV)

		# define range of blue color in HSV
		lower_bound = np.array([100, 40, 0])
		upper_bound = np.array([130, 255, 255])

		# threshold the HSV image to get only blue colors
		img = cv2.inRange(hsv, lower_bound, upper_bound)

		kernel = np.ones((5, 5), np.uint8)
		img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
		img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

		ret, thresh = cv2.threshold(img, 127, 255, 0)
		im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		if len(contours) > 0:
			cnt = contours[0]
			M = cv2.moments(cnt)

			# centroid coords
			cx = int(M['m10'] / M['m00'])
			cy = int(M['m01'] / M['m00'])

			self.objOfInterestFound = True

			cv2.line(croppedCameraImage, (cx, cy), (cx, cy), (0, 0, 255), 20)
			#print cx, cy

		self.IO.imshow('raw', croppedCameraImage)


	def ScanForImages(self, rawCameraImage):
		height, width, channels = rawCameraImage.shape
		w1 = 2 * width / 7
		w2 = 5 * width / 7
		croppedCameraImage = rawCameraImage[0:height, w1:w2]

		cameraImage = cv2.cvtColor(croppedCameraImage, cv2.COLOR_BGR2GRAY)

		# Create SceneData instance
		sceneData = SceneData(cameraImage)

		# look for resources in the scene
		for resourceData in self.resourcesData:
			FeatureMatching(self, resourceData, sceneData)

	def resetVisionFlags(self):
		self.objOfInterestFound = False
		self.visibleResources = [0, 0, 0, 0]

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
				rawCameraImage = self.IO.cameraRead()

				self.resetVisionFlags()

				self.ScanForImages(rawCameraImage)
				if not self.ResourceIsVisible():
					self.ScanForCubeFarAway(rawCameraImage)

				# Dump next couple of frames...
				for i in range(0, 10):
					self.IO.cameraGrab()
#

### eof ###
