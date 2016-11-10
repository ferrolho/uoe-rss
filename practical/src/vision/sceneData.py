from vision.featureMatching import sift

class SceneData:
    def __init__(self, cameraImage):
        # find the keypoints and descriptors of the camera image with SIFT
        keypoints, descriptors = sift.detectAndCompute(cameraImage, None)

        self.image = cameraImage
        self.keypoints = keypoints
        self.descriptors = descriptors
