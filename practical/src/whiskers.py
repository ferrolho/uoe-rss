import threading

# This specifies the number of consecutive state
# occurences required to update the whisker state.
# This is required because the whiskers tend to shake a lot.
SENSOR_THRESHOLD = 6000

# Change the following according to which
# slot each whisker is connected to.
LEFT_SLOT  = 0
RIGHT_SLOT = 1

# Some of the whiskers are bent such that the sensor is
# always triggered. Adjust the settings below accordingly.
LEFT_DEFAULT  = False
RIGHT_DEFAULT = False

class Whiskers:
	def __init__(self, IO):
		Whiskers.IO = IO
		self.left  = Whisker( LEFT_SLOT,  LEFT_DEFAULT)
		self.right = Whisker(RIGHT_SLOT, RIGHT_DEFAULT)

	def __str__(self):
		return '%r %r' % (self.left.state, self.right.state)

class Whisker:
	def __init__(self, sensorSlot, defaultState):
		self.sensorSlot = sensorSlot
		self.counter = 0

		self.defaultState = defaultState
		self.state = defaultState

		t = threading.Thread(target = self.update)
		t.setDaemon(True)
		t.start()

	def update(self):
		while True:
			sensorState = Whiskers.IO.getInputs()[self.sensorSlot]

			if sensorState != self.defaultState:
				if self.counter >= SENSOR_THRESHOLD:
					self.state = True
				else:
					self.counter += 1
			else:
				self.counter = 0
				self.state = False

	def triggered(self):
		return self.state
