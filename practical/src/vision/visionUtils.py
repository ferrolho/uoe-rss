import cv2

from vision.featureMatching import *
from vision.resourceData import *
from vision.sceneData import *

from settings import *

class VisionUtils:
	def __init__(self, IO):
		self.IO = IO
		self.framesProcessed = 0
		self.resourcesData = [ResourceData(name) for name in RESOURCE_NAMES]
		self.deliveryBase = None
		self.resetFlags()

	def resetFlags(self):
		self.centroid_x = None

		# 0 - on the left
		# 1 - aligned (go forward!)
		# 2 - on the right
		self.cubeRelativePos = None

		self.objOfInterestFound = False
		self.visibleResources = [0, 0, 0, 0]

	def process(self, rawCameraImg):
		self.resetFlags()

		self.scanForCartoons(rawCameraImg)

		self.updateDeliveryBase()

		if not self.resourceIsVisible():
			self.scanForCubeFarAway(rawCameraImg)

		self.framesProcessed += 1

	def updateDeliveryBase(self):
		for i, visible in enumerate(self.visibleResources):
			if visible:
				self.deliveryBase = RESOURCE_DEST[i]
				print 'Delivering cube to', self.deliveryBase
				break

	def resourceIsVisible(self):
		for visible in self.visibleResources:
			if visible:
				return True
		return False

	def scanForCartoons(self, rawCameraImg):
		height, width, channels = rawCameraImg.shape

		w1 = 2 * width / 7
		w2 = 5 * width / 7
		croppedImg = rawCameraImg[0:height, w1:w2]

		grayImg = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2GRAY)

		# Create SceneData instance
		sceneData = SceneData(grayImg)

		# look for resources in the scene
		for resourceData in self.resourcesData:
			self.centroid_x = applyFeatureMatching(self, resourceData, sceneData)

			if self.centroid_x:
				print 'Cartoon at', self.centroid_x

				if self.centroid_x <= 100:
					self.cubeRelativePos = 0
				elif 100 <= self.centroid_x <= 170:
					self.cubeRelativePos = 1
				elif self.centroid_x >= 170:
					self.cubeRelativePos = 2

				break

	def scanForCubeFarAway(self, rawCameraImg):
		height, width, channels = rawCameraImg.shape
		croppedImg = rawCameraImg[0:height / 2, 0:width]

		hsv = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2HSV)

		# define range of blue color in HSV
		lower_bound = np.array([100, 40, 0])
		upper_bound = np.array([130, 255, 255])

		# threshold the HSV image to get only blue colors
		img = cv2.inRange(hsv, lower_bound, upper_bound)

		kernel = np.ones((5, 5), np.uint8)
		img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
		img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

		ret, thresh = cv2.threshold(img, 127, 255, 0)
		im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		if len(contours) > 0:
			cnt = contours[0]
			M = cv2.moments(cnt)

			# centroid coords
			cx = int(M['m10'] / M['m00'])
			cy = int(M['m01'] / M['m00'])

			self.objOfInterestFound = True

			cv2.line(croppedImg, (cx, cy), (cx, cy), (0, 0, 255), 20)

			if not self.centroid_x:
				self.centroid_x = cx

				print 'Cube far away at x-', self.centroid_x

				if self.centroid_x <= 220:
					self.cubeRelativePos = 0
				elif 220 <= self.centroid_x <= 420:
					self.cubeRelativePos = 1
				elif self.centroid_x >= 420:
					self.cubeRelativePos = 2

				print 'Cube far away at rel_pos-', self.cubeRelativePos

		self.IO.imshow('raw', croppedImg)
