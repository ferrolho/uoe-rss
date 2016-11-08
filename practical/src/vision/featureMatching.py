import cv2
import numpy as np

from settings import *

MIN_MATCH_COUNT = 5

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

def FeatureMatching(self, resourceData, sceneData):
	matches = flann.knnMatch(resourceData.descriptors, sceneData.descriptors, k = 2)

	# store all the good matches as per Lowe's ratio test.
	good = []
	for m, n in matches:
		if m.distance < 0.7 * n.distance:
			good.append(m)

	matchesMask = None

	if len(good) > MIN_MATCH_COUNT:
		src_pts = np.float32([ resourceData.keypoints[m.queryIdx].pt for m in good ]).reshape(-1, 1, 2)
		dst_pts = np.float32([ sceneData.keypoints[m.trainIdx].pt for m in good ]).reshape(-1, 1, 2)

		M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

		if mask is not None:
			matchesMask = mask.ravel().tolist()

			h, w = resourceData.image.shape
			pts = np.float32([ [0, 0], [0, h-1], [w-1, h-1], [w-1, 0] ]).reshape(-1, 1, 2)
			dst = cv2.perspectiveTransform(pts, M)

			sceneData.image = cv2.polylines(sceneData.image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
			print "%s found!" % resourceData.name

			# save which resources are visible
			for i in range(len(RESOURCE_NAMES)):
				if resourceData.name == RESOURCE_NAMES[i]:
					self.visibleResources[i] = 1

	draw_params = dict(matchColor = (0, 255, 0), # draw matches in green color
					   singlePointColor = None,
					   matchesMask = matchesMask, # draw only inliers
					   flags = 2)

	imgMatches = cv2.drawMatches(resourceData.image, resourceData.keypoints,
								 sceneData.image, sceneData.keypoints,
								 good, None, **draw_params)

	# Display the image
	self.IO.imshow(resourceData.name, imgMatches)
#

### eof ###
