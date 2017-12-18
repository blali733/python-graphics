# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2
import copy

class ImageManager:
    def readImage(self, fileName):
        file = cv2.imread(fileName, 0)
        return file

    def showImage(self, image, title):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def binearizeImage(self, image, offset):
        im = cv2.GaussianBlur(image, (5,5), 0)
        threshold, image = cv2.threshold(im, offset, 255, cv2.THRESH_BINARY)
        return threshold, image

    def findContours(self, image):
        workingCopy = copy.copy(image)
        targetImage, contours, hierarchy = cv2.findContours(workingCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contourPerimeters = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, False)
            contourPerimeters.append(perimeter)
        chosenIndex = 0
        actualIndex = 0
        targetPerimeter = 0
        for perimeter in contourPerimeters:
            if perimeter > targetPerimeter:
                targetPerimeter = perimeter
                chosenIndex = actualIndex
            actualIndex = actualIndex + 1
        
        
            
