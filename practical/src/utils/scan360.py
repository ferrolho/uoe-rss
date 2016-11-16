
def __facingWall(left, right):
	WALL_DIST_THRESHOLD = 180
	return left > WALL_DIST_THRESHOLD and right > WALL_DIST_THRESHOLD

def do360scanToRoom(self, room):
	right, left = self.IO.getSensors()[0], self.IO.getSensors()[1]
	print '{} x {}'.format(left, right)

	if not hasattr(self, '__360scan_started'):
		print '- 360 scan started -'
		self.__360scan_started     = True
		self.__360scan_done        = False
		self.__360scan_state       = 0
		self.__360scan_roomCounter = 0

	if self.__360scan_state == 0:

		# Keeps turning right until the
		# wall keypoint is found.

		self.motors.turnRightOnSpot()

		if __facingWall(left, right):
			print '- FACING WALL -'
			self.__360scan_state += 1
			self.__360scan_minRight = right

	elif self.__360scan_state == 1:

		# Keeps turning right until the
		# right sensor drops to a minimum.

		if right <= self.__360scan_minRight:
			self.__360scan_minRight = right
		else:
			self.__360scan_state += 1

	elif self.__360scan_state == 2:

		# Keeps turning right until the
		# correct opening is detected.

		if room == 'b':
			if left < 200:
				print '- FOUND OPENING TO ROOM B -'
				self.__360scan_state += 1

				#self.hallCounter.setTimerCm(40)
		elif room == 'a' or room == 'c':
			if self.__360scan_roomCounter == 0 and left < 200:
				print '- FOUND OPENING TO ROOM B -'

				self.__360scan_roomCounter += 1

			elif self.__360scan_roomCounter == 1 and left > 200:
				print '- FOUND OPENING TO ROOM A -'

				if room == 'a':
						self.__360scan_state += 1

						#self.hallCounter.setTimerCm(30)
				elif room == 'c':
						self.__360scan_leftFoundGapToRoomA = False
						self.__360scan_roomCounter += 1

			elif self.__360scan_roomCounter == 2:
				if left < 100:
					self.__360scan_leftFoundGapToRoomA = True
				elif self.__360scan_leftFoundGapToRoomA and left > 150:
					print '- FOUND OPENING TO ROOM C -'
					self.__360scan_state += 1

					#self.hallCounter.setTimerCm(0)

	elif self.__360scan_state == 3:

		# 360 scan done.

		self.__360scan_done = True
		self.motors.stop()
		time.sleep(0.2)
