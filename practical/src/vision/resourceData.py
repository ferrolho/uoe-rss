import cv2
from vision.featureMatching import sift

class ResourceData:
    def __init__(self, name):
        image = cv2.imread('resources/' + name + '.png', 0)
        keypoints, descriptors = sift.detectAndCompute(image, None)

        self.name = name
        self.image = image
        self.keypoints = keypoints
        self.descriptors = descriptors
