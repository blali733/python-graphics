import sys
import numpy as np
import cv2
import copy
import math


class ImageCrop:
    def excludeBackground(self, contour, image):
        mask = image.copy()
        mask[mask > 0] = 0
        points = []
        for point in contour:
            points.append([point[2], point[3]])
        polygon = np.array(points, dtype=np.int32)
        cv2.fillPoly(mask, polygon, 255)
        mask = np.logical_not(mask)
        image[mask] = 0
        return image
