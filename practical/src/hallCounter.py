import threading

# The slot the sensor is connected to.
SENSOR_SLOT = 7

class HallCounter:
	def __init__(self, IO):
		self.__IO = IO
		self.__counter = 0
		self.__lastState = self.__IO.getInputs()[SENSOR_SLOT]

		t = threading.Thread(target = self.update)
		t.setDaemon(True)
		t.start()

	def update(self):
		while True:
			sensorState = self.__IO.getInputs()[SENSOR_SLOT]

			if sensorState != self.__lastState:
				self.__counter += 1
				self.__lastState = sensorState
				print 'Travelled distance: %d' % self.__counter

	def getCount(self):
		return self.__counter
