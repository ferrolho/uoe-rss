import time

def goHome(self):

	if not hasattr(self, 'goHome_done'):
		print '- Going home -'
		self.__goHome_state = 0
		self.goHome_done    = False

	sonar = self.sensors[2]

	if self.__goHome_state == 0:

		# turn 180 degrees
		print 'turn 180 degrees'

		self.motors.turnRightOnSpot()

		if sonar > 90:
			self.motors.stop()
			time.sleep(0.1)

			self.__goHome_state += 1

			self.hallCounter.setTimer(20)

	else:
		# use IR sensors
		if self.ObstacleToTheRight():
			self.motors.turnLeftOnSpot()
		elif self.ObstacleToTheLeft():
			self.motors.turnRightOnSpot()
		else:
			if self.__goHome_state == 1:

				# go forward
				print 'go forward'

				self.motors.moveForward()

				if sonar < 50 and self.hallCounter.timerIsDone():
					self.motors.stop()
					time.sleep(0.1)
					self.__goHome_state += 1

			elif self.__goHome_state == 2:

				# turn right
				print 'turn right'

				self.motors.turnRightOnSpot()

				if sonar > 110:
					self.motors.stop()
					time.sleep(0.1)

					self.__goHome_state += 1

					self.hallCounter.setTimer(25)

			elif self.__goHome_state == 3:

				# go forward
				print 'go forward'

				self.motors.moveForward()

				if sonar < 55 and self.hallCounter.timerIsDone():
					self.motors.stop()
					time.sleep(0.1)
					self.__goHome_state += 1

			elif self.__goHome_state == 4:

				# turn right (to home)
				print 'turn right (to home)'

				self.motors.turnRightOnSpot()

				if sonar > 70:
					self.motors.stop()
					time.sleep(0.1)
					self.__goHome_state += 1

			elif self.__goHome_state == 5:

				# go forward 50cm (to home)
				print 'go forward 50cm (to home)'

				self.motors.moveForward()
				self.hallCounter.setTimer(19)
				self.__goHome_state += 1

			elif self.__goHome_state == 6:

				# stop - you got home

				if self.hallCounter.timerIsDone():
					print 'stop - you got home'
					self.motors.stop()
					time.sleep(0.1)
					self.__goHome_state += 1
					self.goHome_done = True
				else:
					self.motors.moveForward()
