# Motors do not have the same power.
# Calibrate them using these parameters.
MOTOR_FILTER_LEFT  = 0.97
MOTOR_FILTER_RIGHT = 1.0

MOTOR_MAX_SPEED = 90
MOTOR_MED_SPEED = MOTOR_MAX_SPEED - 10
MOTOR_LOW_SPEED = MOTOR_MAX_SPEED - 20
MOTOR_SCAN_SPEED = MOTOR_MAX_SPEED - 50

class Motors:
	def __init__(self, IO):
		self.__IO = IO

	def __setSpeeds(self, leftMotor, rightMotor):
		# Attention to how you plug the connectors
		self.__IO.setMotors(MOTOR_FILTER_RIGHT * rightMotor, MOTOR_FILTER_LEFT * leftMotor)

	def stop(self):
		self.__setSpeeds(0, 0)

	def moveBackwards(self):
		self.__setSpeeds(-MOTOR_MAX_SPEED, -MOTOR_MAX_SPEED)
	def moveForward(self):
		self.__setSpeeds( MOTOR_MAX_SPEED,  MOTOR_MAX_SPEED)

	def evadeLeft(self):
		self.__setSpeeds(-MOTOR_MAX_SPEED, -MOTOR_LOW_SPEED)
	def evadeRight(self):
		self.__setSpeeds(-MOTOR_LOW_SPEED, -MOTOR_MAX_SPEED)

	def turnLeft(self):
		self.__setSpeeds(0, MOTOR_MED_SPEED)
	def turnRight(self):
		self.__setSpeeds(MOTOR_MED_SPEED, 0)

	def turnRightOnSpot(self):
		self.__setSpeeds(MOTOR_SCAN_SPEED, -MOTOR_SCAN_SPEED)
