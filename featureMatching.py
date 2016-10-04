import cv2

MIN_MATCH_COUNT = 5

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
