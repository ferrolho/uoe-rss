import threading

# Hall Effect Counter info:
#	1 hall unit = 4 cm

# The slot the sensor is connected to.
SENSOR_SLOT = 7

class HallCounter:
	def __init__(self, IO):
		self.__IO = IO
		self.__lastState = self.__IO.getInputs()[SENSOR_SLOT]
		self.__counter = 0
		self.__timer = 0

		t = threading.Thread(target = self.update)
		t.setDaemon(True)
		t.start()

	def update(self):
		while True:
			sensorState = self.__IO.getInputs()[SENSOR_SLOT]

			if sensorState != self.__lastState:
				self.__lastState = sensorState

				self.__counter += 1
				print 'Travelled distance: %d' % self.__counter

				if self.__timer > 0:
					self.__timer -= 1

	def setTimer(self, units):
		self.__timer = units
	def setTimerCm(self, cm):
		self.__timer = cm / 4
	def timerIsDone(self):
		return self.__timer == 0

	def getCount(self):
		return self.__counter
