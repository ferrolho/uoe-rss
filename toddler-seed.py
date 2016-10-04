#!/usr/bin/env python
__TODDLER_VERSION__ = "1.0.0"

import cv2
import numpy as np
import time

from featureMatching import *
from resourceData import *


def InitResources(resources):
    for name in RESOURCE_NAMES:
        resources.append(ResourceData(name))


def FeatureMatching(self, resourceData, sceneData):
    matches = flann.knnMatch(resourceData.descriptors, sceneData[2], k = 2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
    	if m.distance < 0.7 * n.distance:
    		good.append(m)

    if len(good) > MIN_MATCH_COUNT:
    	src_pts = np.float32([ resourceData.keypoints[m.queryIdx].pt for m in good ]).reshape(-1, 1, 2)
    	dst_pts = np.float32([ sceneData[1][m.trainIdx].pt for m in good ]).reshape(-1, 1, 2)

    	M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    	matchesMask = mask.ravel().tolist()

    	h, w = resourceData.image.shape
    	pts = np.float32([ [0, 0], [0, h-1], [w-1, h-1], [w-1, 0] ]).reshape(-1, 1, 2)
    	dst = cv2.perspectiveTransform(pts, M)

    	sceneData[0] = cv2.polylines(sceneData[0], [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        print "%s found!" % resourceData.name

    else:
    	print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
    	matchesMask = None

    draw_params = dict(matchColor = (0, 255, 0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    imgMatches = cv2.drawMatches(resourceData.image, resourceData.keypoints,
                                 sceneData[0], sceneData[1],
                                 good, None, **draw_params)

    # Display the image
    self.IO.imshow(resourceData.name, imgMatches)


# Main Toddler class
class Toddler:
    # Initialiser
    def __init__(self,IO):
        # Print a message
        print 'I am a toddler playing in a sandbox'

        # Store the instance of IO for later
        self.IO = IO

        # Add more initialisation code here
        self.resourcesData = []
        InitResources(self.resourcesData)


    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Control(self, OK):
        while OK():
            # Add control code here
            time.sleep(0.05)


    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Vision(self, OK):
        # Set the camera resolution
        self.IO.cameraSetResolution('low')

        while OK():
            # Grab the image
            self.IO.cameraGrab()

            # Read the image
            cameraImage = cv2.cvtColor(self.IO.cameraRead(), cv2.COLOR_BGR2GRAY)

            # find the keypoints and descriptors of the camera image with SIFT
            kp, des = sift.detectAndCompute(cameraImage, None)

            # [cameraImage, keypoints, descriptors]
            cameraData = [cameraImage, kp, des]

            # look for resources in the scene
            for resourceData in self.resourcesData:
                FeatureMatching(self, resourceData, cameraData)

            # Dump next couple of frames...
            for i in range(0, 10):
                self.IO.cameraGrab()
#

### eof ###
