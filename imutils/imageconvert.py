from medpy.io import load
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from . import medimageservicing as msc
import cv2
try:
    from osutils import windows as osutil
except ImportError:
    from osutils import posix as osutil


class ImageConvert:
    def __init__(self):
        self.image_count = 0
        self.processed_image_count = 0

    def main(self):
        print("Please provide input directory for images")

    def info(self):
        print("Processing image "+self.processed_image_count.__str__()+" of "+self.image_count.__str__())
        print()
        print("Key bindings:")
        print("X - breaks execution")
        print("0 - saves image")
        print("1 - discards image")

    def prepareSlices(self, path, image, spacing=1):
        i, h = load(path+"/"+image)
        mmax = i.max()
        mmin = i.min()
        for a in range(i.shape[0]):
            for b in range(i.shape[1]):
                for c in range(i.shape[2]):
                    i[a, b, c] = (i[a, b, c] - mmin) / mmax * 255
        # k = i[27, :, :]
        i = np.uint8(i)
        for j in range(int(i.shape[0] / spacing)):
            cv2.imwrite("data/raw/out/" + image + (j*spacing).__str__() + ".jpg", i[j * spacing, :, :])
