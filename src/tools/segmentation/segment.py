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
    def squared_histogram_equalization(self, image):
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        hist = np.sqrt(hist)
        cdf = hist.cumsum()
        cdf_normalized = cdf * float(hist.max()) / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        image_equalized = cdf[image]
        return image_equalized

    def gamma_correction(self, image, gamma=1.0):
        table = np.array([((i / 255.0) ** gamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def maximum_entropy_thresholding(self, image):
        hist, bins = np.histogram(image.flatten(), 256, normed=True, range=[0, 256])
        epsilon = np.finfo(dtype=np.double).min
        group_probability = np.zeros(hist.shape, dtype=np.double)
        group_probability[0] = hist[0]
        entropy_black = np.zeros(hist.shape, dtype=np.double)
        entropy_white = np.zeros(hist.shape, dtype=np.double)

        # prawdopodobienstwo wystapienia danych wartosci grupowo
        for i in range(1, len(group_probability)):
            group_probability[i] = group_probability[i-1] + hist[i]

        for i in range(0, len(group_probability)):
            if np.greater(group_probability[i], epsilon):
                entropy_internal_black = 0.0
                # prawdopodobienstwo pojedynczego elementu w stosunku do prawdopodobienstwa grupy
                for j in range(0, i + 1):
                    if np.greater(hist[j], epsilon):
                        group_multiplier = 1.0 / group_probability[i]
                        element_probability = hist[j] * group_multiplier
                        if np.greater(element_probability, 0):
                            entropy_internal_black = entropy_internal_black - element_probability * np.log2(
                                element_probability)
                entropy_black[i] = entropy_internal_black

            probability_white = 1 - group_probability[i]
            if np.greater(probability_white, epsilon):
                entropy_internal_white = 0.0
                for j in range(i + 1, len(group_probability)):
                    if np.greater(hist[j], epsilon):
                        group_multiplier = 1.0 / probability_white
                        element_probability = hist[j] * group_multiplier
                        if np.greater(element_probability, 0):
                            entropy_internal_white = entropy_internal_white - element_probability * np.log2(
                                element_probability)
                entropy_white[i] = entropy_internal_white

        max_entropy = entropy_black[0] + entropy_white[0]
        max_entropy_index = 0

        for i in range(1, len(group_probability)):
            max_entropy_internal = entropy_black[i] + entropy_white[i]
            if max_entropy_internal > max_entropy:
                max_entropy = max_entropy_internal
                max_entropy_index = i
        return cv2.threshold(image, max_entropy_index, 255, cv2.THRESH_BINARY)

    # def startSegmentation(self):
    #     image = cv2.imread('flair_segment1.png', 0)
    #     median_kernel_size = 11
    #     gamma_correction = 5
    #     image_blured = cv2.medianBlur(image, median_kernel_size)
    #     image_equalized = self.squared_histogram_equalization(image_blured)
    #     image_gamma_corrected = self.gamma_correction(image_equalized, gamma_correction)
    #     ret, image_entropy_thresholded = self.maximumEntropyThresholding(image_gamma_corrected)
    #     cv2.imshow('original', image)
    #     cv2.imshow('blured', image_blured)
    #     cv2.imshow('equalized', image_equalized)
    #     cv2.imshow('gamma_corrected', image_gamma_corrected)
    #     cv2.imshow('thresholded', image_entropy_thresholded)
    #
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     app = Segmentation()
#     app.startSegmentation()

