from src.tools.mha import mhaMath
import cv2
import numpy as np

def flair(image_slice):
    """
    Method responsible for segmentation of FLAIR image.

    Parameters
    ----------
    image_slice : np.array
        Image slice to be processed.

    Returns
    -------
    np.array
        Binearized array.
    """
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.047)*(img > 0.016)*1


def t1(image_slice):
    """
    Method responsible for segmentation of T1 image.

    Parameters
    ----------
    image_slice : np.array
        Image slice to be processed.

    Returns
    -------
    np.array
        Binearized array.
    """
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.0323) * (img > 0.0144) * 1


def t1c(image_slice):
    """
    Method responsible for segmentation of T1C image.

    Parameters
    ----------
    image_slice : np.array
        Image slice to be processed.

    Returns
    -------
    np.array
        Binearized array.
    """
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.045) * (img > 0.019) * 1


def t2(image_slice):
    """
    Method responsible for segmentation of T2 image.

    Parameters
    ----------
    image_slice : np.array
        Image slice to be processed.

    Returns
    -------
    np.array
        Binearized array.
    """
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.05) * (img > 0.022) * 1

class Segmentation:
    def squaredHistogramEqualization(self, image):
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        hist = np.sqrt(hist)
        cdf = hist.cumsum()
        cdf_normalized = cdf * float(hist.max()) / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        image_equalized = cdf[image]
        return image_equalized

    def gammaCorrection(self, image, gamma=1.0):
        table = np.array([((i / 255.0) ** gamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def maximumEntropyThresholding(self, image):
        hist, bins = np.histogram(image.flatten(), 256, normed=True, range=[0, 256])
        epsilon = np.finfo(dtype=np.double).min
        groupProbability = np.zeros(hist.shape, dtype=np.double)
        groupProbability[0] = hist[0]
        entropyBlack = np.zeros(hist.shape, dtype=np.double)
        entropyWhite = np.zeros(hist.shape, dtype=np.double)

        # prawdopodobienstwo wystapienia danych wartosci grupowo
        for i in range(1, len(groupProbability)):
            groupProbability[i] = groupProbability[i-1] + hist[i]

        for i in range(0, len(groupProbability)):
            if np.greater(groupProbability[i], epsilon):
                entropyInternalBlack = 0.0
                # prawdopodobienstwo pojedynczego elementu w stosunku do prawdopodobienstwa grupy
                for j in range(0, i + 1):
                    if np.greater(hist[j], epsilon):
                        groupMultiplier = 1.0 / groupProbability[i]
                        elementProbability = hist[j] * groupMultiplier
                        if np.greater(elementProbability, 0):
                            entropyInternalBlack = entropyInternalBlack - elementProbability * np.log2(elementProbability)
                entropyBlack[i] = entropyInternalBlack

            probabilityWhite = 1 - groupProbability[i]
            if np.greater(probabilityWhite, epsilon):
                entropyInternalWhite = 0.0
                for j in range(i + 1, len(groupProbability)):
                    if np.greater(hist[j], epsilon):
                        groupMultiplier = 1.0 / probabilityWhite
                        elementProbability = hist[j] * groupMultiplier
                        if np.greater(elementProbability, 0):
                            entropyInternalWhite = entropyInternalWhite - elementProbability * np.log2(elementProbability)
                entropyWhite[i] = entropyInternalWhite

        maxEntropy = entropyBlack[0] + entropyWhite[0]
        maxEntropyIndex = 0

        for i in range(1, len(groupProbability)):
            maxEntropyInternal = entropyBlack[i] + entropyWhite[i]
            if maxEntropyInternal > maxEntropy:
                maxEntropy = maxEntropyInternal
                maxEntropyIndex = i
        return cv2.threshold(image, maxEntropyIndex, 255, cv2.THRESH_BINARY)

    def startSegmentation(self):
        image = cv2.imread('flair_segment1.png', 0)
        median_kernel_size = 11
        gamma_correction = 5
        image_blured = cv2.medianBlur(image, median_kernel_size)
        image_equalized = self.squaredHistogramEqualization(image_blured)
        image_gamma_corrected = self.gammaCorrection(image_equalized, gamma_correction)
        ret, image_entropy_thresholded = self.maximumEntropyThresholding(image_gamma_corrected)
        cv2.imshow('original', image)
        cv2.imshow('blured', image_blured)
        cv2.imshow('equalized', image_equalized)
        cv2.imshow('gamma_corrected', image_gamma_corrected)
        cv2.imshow('thresholded', image_entropy_thresholded)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = Segmentation()
    app.startSegmentation();

