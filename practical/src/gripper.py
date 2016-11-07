SERVO_POS_OPEN  = 130
SERVO_POS_CLOSE = 70

class Gripper:
	def __init__(self, IO):
		self.IO = IO
		self.IO.servoEngage()
		self.open()

	def __del__(self):
		self.IO.servoDisengage()

	def close(self):
		self.opened = False
	def open(self):
		self.opened = True
	def update(self):
		self.IO.servoSet(SERVO_POS_OPEN if self.isOpened() else SERVO_POS_CLOSE)

	def isOpened(self):
		return self.opened
	def isClosed(self):
		return not self.opened
