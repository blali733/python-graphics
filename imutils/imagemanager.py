# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2
import copy
import math

class ImageManager:
    def rad2deg(self, anglerad):
        angledeg = anglerad*180/math.pi + 180
        return angledeg

    def getKey(self, item):
        return item[1]

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
        return contours
        
    def contours2angdist(self, contours, centerX, centerY):
        newContours=[]
        for contour in contours:
            for i in range(0, contour.shape[0]-1):
                x = contour[i, 0, 0]
                y = contour[i, 0, 1]
                dist = math.sqrt(math.pow(x+centerX, 2)+math.pow(y+centerY, 2))
                anglerad = math.atan2(y-centerY, x-centerX)
                newContours.append([dist, self.rad2deg(anglerad), x, y])
        newContours = sorted(newContours, key=self.getKey)
        return newContours

    def checkPoint(self, chosenPoint, point, targetDistance, offset):
        newChosenPoint = chosenPoint
        newTargetDistance = targetDistance
        conditionIsMet = False
        if point[0] <= targetDistance:
            newChosenPoint = point
            newTargetDistance = point[0]
        if newTargetDistance >= offset:
            conditionIsMet = True
        return newChosenPoint, newTargetDistance, conditionIsMet

    def choosePointsForExpectingContour(self, contours, offset):
        expectedContours = []
        targetAngle = contours[0][1]
        targetDistance = contours[0][0]
        chosenPoint = contours[0]
        conditionIsMet = False
        for i in range(0, len(contours) - 1):
            if contours[i][1] <= (targetAngle + 0.5):
                chosenPoint, targetDistance, conditionIsMet = self.checkPoint(chosenPoint, contours[i], targetDistance, offset)
            else:
                targetAngle = contours[i][1]
                targetDistance = contours[i][0]
                if conditionIsMet:
                    expectedContours.append(chosenPoint)
                conditionIsMet = False
                chosenPoint, targetDistance, conditionIsMet = self.checkPoint(chosenPoint, contours[i], targetDistance, offset)
        return expectedContours