import time

def aToHome(self):

	if not hasattr(self, 'aToHome_done'):
		print '- Going home from A -'
		self.__aToHome_state = 0
		self.aToHome_done    = False

	sonar = self.sensors[2]

	# use IR sensors
	if self.ObstacleToTheRight():
		self.motors.turnLeftOnSpot()
	elif self.ObstacleToTheLeft():
		self.motors.turnRightOnSpot()
	else:
		if self.__aToHome_state == 0:

			# go backwards
			print 'go backwards'

			self.motors.moveBackwards()

			if sonar > 90:
				self.motors.stop()
				time.sleep(0.1)
				self.__aToHome_state += 2

		elif self.__aToHome_state == -1:

			# turn left (to corner)
			print 'turn left (to corner)'

			self.motors.turnLeftOnSpot()

			if sonar < 50:
				self.motors.stop()
				time.sleep(0.1)
				self.__aToHome_state += 1

		elif self.__aToHome_state == 2:

			# turn left (to home)
			print 'turn left (to home)'

			self.motors.turnLeftOnSpot()
			time.sleep(1.6)

			self.motors.stop()
			time.sleep(0.1)

			self.__aToHome_state += 1

		elif self.__aToHome_state == 3:

			# go forward (to home)
			print 'go forward (to home)'

			self.motors.moveForward()
			self.hallCounter.setTimer(18)
			self.__aToHome_state += 1

		elif self.__aToHome_state == 4:

			# stop - you got home

			if sonar < 25 or self.hallCounter.timerIsDone():
				print 'stop - you got home'
				self.motors.stop()
				time.sleep(0.1)
				self.__aToHome_state += 1
				self.aToHome_done = True
			else:
				self.motors.moveForward()
