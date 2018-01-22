import numpy as np
import cv2
from pimutils.mha import mhaMath

# below values for threshold for considered images
    # flair - 187
    # t1 - 205
    # t1c - 160
    # t2 - 160


def flair(image_slice):
    img = mhaMath.med_2_uint8(image_slice)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 187, 255, cv2.THRESH_BINARY)
    return mhaMath.med_image_binearize(th)


def t1(image_slice):
    img = mhaMath.med_2_uint8(image_slice)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 205, 255, cv2.THRESH_BINARY)
    return mhaMath.med_image_binearize(th)


def t1c(image_slice):
    img = mhaMath.med_2_uint8(image_slice)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)
    return mhaMath.med_image_binearize(th)


def t2(image_slice):
    img = mhaMath.med_2_uint8(image_slice)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)
    return mhaMath.med_image_binearize(th)
