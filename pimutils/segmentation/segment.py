import numpy as np
#from pimutils import medimageservicing as msc
import cv2

def flair(image_slice):
    output_array = np.zeros(image_slice.shape, dtype=image_slice.dtype)
    for y in range(image_slice.shape[1]):
        for x in range(image_slice.shape[0]):
            if image_slice[y, x] >= 750:
                output_array[y, x] = 1
            else:
                output_array[y, x] = 0
    return output_array


def t1(image_slice):
    output_array = np.zeros(image_slice.shape, dtype=image_slice.dtype)
    return output_array


def t1c(image_slice):
    return np.zeros(image_slice.shape, dtype=image_slice.dtype)


def t2(image_slice):
    return np.zeros(image_slice.shape, dtype=image_slice.dtype)

