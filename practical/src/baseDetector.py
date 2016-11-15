import threading

# When the sensors measure light below this
# threshold, they will assume it is a black base.
SENSOR_THRESHOLD = 15

# Change the following according to which
# slot each sensor is connected to.
LEFT_SLOT  = 4
RIGHT_SLOT = 5

class BaseDetector:
	def __init__(self, IO):
		BaseDetector.IO = IO
		self.left  = Sensor( LEFT_SLOT)
		self.right = Sensor(RIGHT_SLOT)

	def __str__(self):
		return 'Base Detector - %r %r' % (self.left.lightSample, self.right.lightSample)

class Sensor:
	def __init__(self, sensorSlot):
		self.sensorSlot = sensorSlot
		self.lightSample = None

		t = threading.Thread(target = self.update)
		t.setDaemon(True)
		t.start()

	def update(self):
		while True:
			self.lightSample = BaseDetector.IO.getSensors()[self.sensorSlot]

	def triggered(self):
		return self.lightSample <= SENSOR_THRESHOLD
