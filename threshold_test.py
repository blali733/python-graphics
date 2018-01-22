import cv2
from matplotlib import pyplot as plt
import segmentationTest
from pimutils.mha import mhaMath

slices_flair = segmentationTest.flair_slices
slices_t1 = segmentationTest.t1_slices
slices_t1c = segmentationTest.t1c_slices
slices_t2 = segmentationTest.t2_slices

for slice in slices_t1:
    img = mhaMath.med_2_uint8(slice)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    #below values for threshold for considered images
    #flair - 187
    #t1 - 205
    #t1c - 160
    #t2 - 160
    ret, th = cv2.threshold(blur, 205, 255, cv2.THRESH_BINARY)
    image = [th]
    for im in image:
        plt.imshow(im, cmap=plt.cm.Greys)
        plt.show()
