from medpy.io import load
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import cv2


class ImageConvert:
    def main(self):
        pass

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
