
# Import the libraries
import cv2
import os
import numpy as np

class SURF:
    """
    Class that provides easy access to the SURF algorithm
    """

    def __init__(self, hessianThreshold=100, nOctaves=4, nOctaveLayers=3, extended=False, upright=False, distance=cv2.NORM_L2, crossCheck=False):
        """
        Set the default values
        """
        if hessianThreshold < 0:
            hessianThreshold = 0
        if nOctaves < 0:
            nOctaves = 0
        if nOctaveLayers < 0:
            nOctaveLayers = 0

        # Creates the SURF object
        self.faceRec = cv2.xfeatures2d.SURF_create(hessianThreshold=hessianThreshold, nOctaves=nOctaves, nOctaveLayers=nOctaveLayers, extended=extended, upright=upright)

        # Creates the matcher object
        self.matcher = cv2.BFMatcher(distance, crossCheck=crossCheck)

        self.labels = []
        self.algorithmTrained = False

    def getAlgorithmName(self):
        return "Speeded Up Robust Features (SURF)"

    def train(self, images, labels):
        """
        Train the face recognition algorithm
        """
        self.labels = labels

        for image in images:

            # Detects and computes the keypoints and descriptors using the SURF algorithm
            keypoints, descriptors = self.faceRec.detectAndCompute(image, None)
    
            # Creates an numpy array
            clusters = np.array([descriptors])

            # Add the array to the BFMatcher
            self.matcher.add(clusters)

        # Train: Does nothing for BruteForceMatcher though
        self.matcher.train()
        self.algorithmTrained = True

    def predict(self, image):
        """
        Predict the image
        """
        if self.algorithmTrained is False:
            print "The face recognition algorithm was not trained."
            sys.exit()

        # Detects and computes the keypoints and descriptors using the SURF algorithm
        keypoints, descriptors = self.faceRec.detectAndCompute(image, None)
    
        # Get all matches based on the descriptors
        matches = self.matcher.match(descriptors)

        # Order by distance
        matches = sorted(matches, key = lambda x:x.distance)
    
        # Creates a results vector to store the number of similar points for each image on the training set
        results = [0]*len(self.labels)

        # Based on the matches vector we create the results vector that represents how many points this test image are similar to each image in the training set
        for match in matches:
            results[match.imgIdx] += 1

        # Index receives the position of the maximum value in the results vector (it means that this is the most similar image)
        index = results.index(max(results))

        return self.labels[index], max(results)
