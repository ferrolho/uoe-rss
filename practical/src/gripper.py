class Gripper:
	def __init__(self, IO):
		self.IO = IO
		self.IO.servoEngage()
		self.open()

	def __del__(self):
		self.IO.servoDisengage()

	def close(self):
		self.IO.servoSet(70)
		self.opened = False
	def open(self):
		self.IO.servoSet(130)
		self.opened = True

	def isOpened(self):
		return self.opened
	def isClosed(self):
		return not self.opened
