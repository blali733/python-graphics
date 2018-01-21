import cv2
from matplotlib import pyplot as plt
import segmentationTest
from pimutils.mha import mhaMath

slices = segmentationTest.flair_slices
for slice in slices:
    img = mhaMath.med_2_uint8(slice)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 187, 255, cv2.THRESH_BINARY)
    image = [th]
    for im in image:
        plt.imshow(im, cmap=plt.cm.Greys)
        plt.show()
