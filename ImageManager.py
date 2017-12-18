# -*- coding: utf-8 -*-
import sys
import cv2

class ImageManager:
    def readImage(fileName):
        file = cv2.imread(fileName, 0)
        return file