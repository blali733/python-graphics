import cv2
import numpy as np
from matplotlib import pyplot as plt
import segmentationTest
from pimutils.mha import mhaMath

slices = segmentationTest.flair_slices
for slice in slices:
    img = mhaMath.med_2_uint8(slice)
    ret, th = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    image = [th]
    for im in image:
        print(im)
        plt.imshow(im.reshape(im.shape[0], im.shape[1]), cmap=plt.cm.Greys)
