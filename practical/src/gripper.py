# When the gripper sensor measures light below this
# threshold, it will assume there is a cube on the gripper dock.
SENSOR_THRESHOLD = 40

# Servo positions to open/close the gripper.
SERVO_POS_OPEN  = 130
SERVO_POS_CLOSE = 70

# The slot the sensor is connected to.
SENSOR_SLOT = 3

class Gripper:
	def __init__(self, IO):
		self.IO = IO
		self.IO.servoEngage()
		self.open()

	def __del__(self):
		self.IO.servoDisengage()

	def open(self):
		self.opened = True
	def close(self):
		self.opened = False
	def update(self):
		self.IO.servoSet(SERVO_POS_OPEN if self.isOpened() else SERVO_POS_CLOSE)

	def openNow(self):
		self.open()
		self.update()
	def closeNow(self):
		self.close()
		self.update()

	def isOpened(self):
		return self.opened
	def isClosed(self):
		return not self.opened

	def sensesCube(self):
		return self.IO.getSensors()[SENSOR_SLOT] < SENSOR_THRESHOLD
	def isTransportingCube(self):
		return self.sensesCube() and self.isClosed()
