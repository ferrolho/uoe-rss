#!/usr/bin/env python
__TODDLER_VERSION__="1.0.0"

import cv2
import numpy as np
import time

MIN_MATCH_COUNT = 5

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

def FeatureMatching(self, windowTitle, queryImage, sceneImage):
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(queryImage,None)
    kp2, des2 = sift.detectAndCompute(sceneImage,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
    	if m.distance < 0.7 * n.distance:
    		good.append(m)

    #

    if len(good) > MIN_MATCH_COUNT:
    	src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    	dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    	M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    	matchesMask = mask.ravel().tolist()

    	h,w = queryImage.shape
    	pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    	dst = cv2.perspectiveTransform(pts,M)

    	sceneImage = cv2.polylines(sceneImage,[np.int32(dst)],True,255,3, cv2.LINE_AA)

        print "%s found!" % windowTitle

    else:
    	print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
    	matchesMask = None

    #

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    imgMatches = cv2.drawMatches(queryImage,kp1,sceneImage,kp2,good,None,**draw_params)

    # Display the image
    self.IO.imshow(windowTitle, imgMatches)

#

RESOURCE_NAMES = ['mario', 'wario', 'watching', 'zoidberg']

# Main Toddler class
class Toddler:
    # Initialiser
    def __init__(self,IO):
        # Print a message
        print 'I am a toddler playing in a sandbox'
        # Store the instance of IO for later
        self.IO=IO

        # Add more initialisation code here
        self.resources = []
        for resourceName in RESOURCE_NAMES:
            imgPath = 'resources/' + resourceName + '.png'
            self.resources.append((resourceName, cv2.imread(imgPath, 0)))


    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Control(self, OK):
        while OK():
            # Add control code here
            time.sleep(0.05)

    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Vision(self, OK):
        # Set the resolution to low
        self.IO.cameraSetResolution('low')

        while OK():
            # Grab the image
            self.IO.cameraGrab()

            # Read the image
            cameraImage = self.IO.cameraRead()

            for resource in self.resources:
                FeatureMatching(self, resource[0], resource[1], cameraImage)

            # Dump next couple of frames...
            for i in range(0, 10):
                self.IO.cameraGrab()
