import time

def __facingWall(left, right):
	WALL_DIST_THRESHOLD = 180
	return left > WALL_DIST_THRESHOLD and right > WALL_DIST_THRESHOLD

def scan360toRoom(self, room):
	right, left = self.IO.getSensors()[0], self.IO.getSensors()[1]
	print '{} x {}'.format(left, right)

	if not hasattr(self, 'scan360_done'):
		print '- Scanning 360 to room -'
		self.__scan360_state       = 0
		self.__scan360_roomCounter = 0
		self.scan360_done          = False

	if self.__scan360_state == 0:

		# Keeps turning right until the
		# wall keypoint is found.

		self.motors.turnRightOnSpot()

		if __facingWall(left, right):
			print '- FACING WALL -'
			self.__scan360_minRight = right
			self.__scan360_state += 1

	elif self.__scan360_state == 1:

		# Keeps turning right until the
		# right sensor drops to a minimum.

		if right <= self.__scan360_minRight:
			self.__scan360_minRight = right
		else:
			self.__scan360_state += 1

	elif self.__scan360_state == 2:

		# Keeps turning right until the
		# correct opening is detected.

		if room == 'b':
			if left < 180:
				print '- FOUND OPENING TO ROOM B -'
				self.__scan360_state += 1

		elif room == 'a' or room == 'c':
			if self.__scan360_roomCounter == 0 and left < 180:
				print '- FOUND OPENING TO ROOM B -'
				self.__scan360_roomCounter += 1

			elif self.__scan360_roomCounter == 1 and left > 200:
				print '- FOUND OPENING TO ROOM A -'

				if room == 'a':
						self.__scan360_state += 1

				elif room == 'c':
						self.__scan360_leftFoundGapToRoomA = False
						self.__scan360_roomCounter += 1

			elif self.__scan360_roomCounter == 2:
				if left < 100:
					self.__scan360_leftFoundGapToRoomA = True
				elif self.__scan360_leftFoundGapToRoomA and left > 150:
					print '- FOUND OPENING TO ROOM C -'
					time.sleep(0.2)
					self.__scan360_state += 1

	elif self.__scan360_state == 3:

		# 360 scan done.

		self.scan360_done = True
		self.motors.stop()
		time.sleep(0.2)
