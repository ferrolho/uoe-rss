import time

def moveFromHomeToRoom(self, room):

	if not hasattr(self, 'moveFromHomeToRoom_done'):
		print '- Moving from home to room -'
		self.__moveFromHomeToRoom_state = 0
		self.moveFromHomeToRoom_done    = False

	if self.__moveFromHomeToRoom_state == 0:

		# Go forward for X cm
		#  - Requires being faced to the right position

		if room == 'a':
			self.hallCounter.setTimerCm(40)
		elif room == 'b':
			self.hallCounter.setTimerCm(55)
		elif room == 'c':
			self.hallCounter.setTimerCm(0)

		self.motors.moveForward()

		self.__moveFromHomeToRoom_state += 1

	elif self.__moveFromHomeToRoom_state == 1:

		# Turn robot to face the middle of the room

		if room == 'a':
			if self.ObstacleToTheRight():
				self.motors.turnLeftOnSpot()
			elif self.ObstacleToTheLeft():
				self.motors.turnRightOnSpot()
			else:
				self.motors.moveForward()

		if self.hallCounter.timerIsDone():
			self.motors.stop()

			if room == 'b':
				self.hallCounter.setTimer(2)
				self.motors.turnLeft()

			self.__moveFromHomeToRoom_state += 1

	elif self.__moveFromHomeToRoom_state == 2:

		# That's it. Done.

		if self.hallCounter.timerIsDone():
			self.motors.stop()

			self.moveFromHomeToRoom_done = True
