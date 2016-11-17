import time

def __waitForNewFrame(self):
	lastFrameID = self.visionUtils.framesProcessed
	print 'Waiting for next frame'
	while lastFrameID == self.visionUtils.framesProcessed:
		time.sleep(0.1)
	print 'New frame!'

def fetchCube(self, room):

	if not hasattr(self, 'fetchCube_done'):
		print '- Moving from home to room -'
		self.__fetchCube_state = 0
		self.__fetchCube_cubeHasBeenSeen = False
		self.fetchCube_done    = False

	if self.__fetchCube_state == 0:

		# Looking for the cube

		__waitForNewFrame(self)

		if self.visionUtils.cubeRelativePos is None:
			if room == 'b':
				self.motors.turnLeft()
			elif room == 'a' or room == 'c':
				self.motors.turnRight()

			time.sleep(0.1)
			self.motors.stop()
		else:
			self.__fetchCube_cubeHasBeenSeen = True
			self.__fetchCube_state += 1

	elif self.__fetchCube_state == 1:

		# Approaching the cube

		if self.gripper.sensesCube():
			# Cube on the gripper dock already - skip this state
			self.__fetchCube_state += 1
		else:
			__waitForNewFrame(self)

			if self.visionUtils.cubeRelativePos is not None:
				print 'Testing - %d' % self.visionUtils.cubeRelativePos

				if self.visionUtils.cubeRelativePos == 1:
					print 'go a bit more'
					self.motors.moveForward()
					self.hallCounter.setTimerAndWait(4)
				else:
					if self.visionUtils.cubeRelativePos == 0:
						print 'turnLeft'
						self.motors.turnLeft()
					elif self.visionUtils.cubeRelativePos == 2:
						print 'turnRight'
						self.motors.turnRight()

					time.sleep(0.1)

				self.motors.stop()
			else:
				# Do we have the cube alread?
				self.__fetchCube_state += 1

	elif self.__fetchCube_state == 2:

		# Cube is in the gripper dock - grab it!

		time.sleep(0.1)

		if self.gripper.sensesCube():
			self.gripper.close()
			self.motors.stop()
			print '- GOT DA CUBE -'
			self.fetchCube_done = True
		else:
			self.__fetchCube_state += 1

	elif self.__fetchCube_state == 3:

		# Cube no longer in the frame - we must be just about to catch it

		self.motors.moveForward()
		self.hallCounter.setTimer(5)

		while not self.hallCounter.timerIsDone() and not self.gripper.sensesCube():
			time.sleep(0.1)
		self.motors.stop()
		time.sleep(0.5)

		if self.gripper.sensesCube():
			self.__fetchCube_state -= 1
		else:
			# we did not catch it - go back and try again
			self.motors.moveBackwards()
			self.hallCounter.setTimerAndWait(8)
			self.motors.stop()
			self.__fetchCube_state = 1
