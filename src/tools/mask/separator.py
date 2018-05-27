import numpy as np
from src.tools.mask import comparator
from src.tools.matrix import resizer


class Separator:
    def __init__(self, min_area):
        """
        Creates instance of class

        Parameters
        ----------
        min_area : int
            Value defining minimal pixel count of stain to be counted as valid, parts with lower pixel count would be
            discarded
        """
        self.min_area = min_area

    def check_neighbourhood(self, data_mask, stain_mask, pixels: list, boundaries):
        """
        Method checks all pixels in neighbourhood and determines if they are part of mask (1's)

        Parameters
        ----------
        data_mask : np.array
            Mask obtained from image slice.
        stain_mask : np.array
            Mask of current stain.
        pixels : list of tuples
            List of pixels to be checked.
        boundaries : tuple of 4 ints
            Contains 4 ints: lowx, hix, lowy, hiy.

        Returns
        -------
        Modified set of parameters, maintaining order.
        """
        tx = pixels[0][0]
        ty = pixels[0][1]
        lowx = boundaries[0]
        hix = boundaries[1]
        lowy = boundaries[2]
        hiy = boundaries[3]
        # left
        try:
            if data_mask[tx - 1, ty] == 1:
                stain_mask[tx - 1, ty] = 1
                pixels.append((tx - 1, ty))
                data_mask[tx - 1, ty] = 0
                if tx - 1 < lowx:
                    lowx = tx - 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # top - left
        try:
            if data_mask[tx - 1, ty - 1] == 1:
                stain_mask[tx - 1, ty - 1] = 1
                pixels.append((tx - 1, ty - 1))
                data_mask[tx - 1, ty - 1] = 0
                if tx - 1 < lowx:
                    lowx = tx - 1
                if ty - 1 < lowy:
                    lowy = ty - 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # top
        try:
            if data_mask[tx, ty - 1] == 1:
                stain_mask[tx, ty - 1] = 1
                pixels.append((tx, ty - 1))
                data_mask[tx, ty - 1] = 0
                if ty - 1 < lowy:
                    lowy = ty - 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # top - right
        try:
            if data_mask[tx + 1, ty - 1] == 1:
                stain_mask[tx + 1, ty - 1] = 1
                pixels.append((tx + 1, ty - 1))
                data_mask[tx + 1, ty - 1] = 0
                if tx + 1 > hix:
                    hix = tx + 1
                if ty - 1 < lowy:
                    lowy = ty - 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # right
        try:
            if data_mask[tx + 1, ty] == 1:
                stain_mask[tx + 1, ty] = 1
                pixels.append((tx + 1, ty))
                data_mask[tx + 1, ty] = 0
                if tx + 1 > hix:
                    hix = tx + 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # bottom - right
        try:
            if data_mask[tx + 1, ty + 1] == 1:
                stain_mask[tx + 1, ty + 1] = 1
                pixels.append((tx + 1, ty + 1))
                data_mask[tx + 1, ty + 1] = 0
                if tx + 1 > hix:
                    hix = tx + 1
                if ty + 1 > hiy:
                    hiy = ty + 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # bottom
        try:
            if data_mask[tx, ty + 1] == 1:
                stain_mask[tx, ty + 1] = 1
                pixels.append((tx, ty + 1))
                data_mask[tx, ty + 1] = 0
                if ty + 1 > hiy:
                    hiy = ty + 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        # bottom - left
        try:
            if data_mask[tx - 1, ty + 1] == 1:
                stain_mask[tx - 1, ty + 1] = 1
                pixels.append((tx - 1, ty + 1))
                data_mask[tx - 1, ty + 1] = 0
                if tx - 1 < lowx:
                    lowx = tx - 1
                if ty + 1 > hiy:
                    hiy = ty + 1
        except IndexError:  # In case of addressing pixel not in range
            pass
        return data_mask, stain_mask, pixels, (lowx, hix, lowy, hiy)

    def get_list_of_stains(self, two_layer_image):
        """
        Separates stains from cumulative image.

        Requires second "mask" layer in binearized form

        Parameters
        ----------
        two_layer_image : tuple
            Tuple of two images, namely slice of brain and its mask

        Returns
        -------
        list
            List of tuples in form: nparray, nparray, int, int containing masked image fragment, mask fragment, y and x
            (numpy compatible addressing) of left upper corner of fragment in whole image
        """
        stains = []  # List of results
        pixels = []  # List of neighbouring unchecked pixels as address tuples
        image = two_layer_image[0]
        mask = np.copy(two_layer_image[1]).astype(two_layer_image[1].dtype)
        temp_mask = np.zeros(mask.shape, dtype=mask.dtype)
        if mask.max() == 1:
            for x in range(mask.shape[0]-1):
                if mask[x, :].max() == 1:
                    for y in range(mask.shape[1] - 1):
                        if mask[x, y] == 1:  # Got hit
                            # Copy address values
                            lowx = x  # Would be set to left border of image
                            lowy = y  # Would be set to top border of image
                            hix = x   # Would be set to right border of image
                            hiy = y   # Would be set to bottom border of image
                            borders = (lowx, hix, lowy, hiy)
                            # Activate in new mask
                            mask[x, y] = 0
                            temp_mask[lowx, lowy] = 1
                            # Add to list of pixels waiting for neighbourhood check
                            pixels.append((lowx, lowy))
                            while len(pixels) > 0:  # Check neighbours
                                tx = pixels[0][0]
                                ty = pixels[0][1]
                                mask, temp_mask, pixels, borders = self.check_neighbourhood(mask, temp_mask, pixels,
                                                                                            borders)
                                pixels.pop(0)  # Remove checked pixel from list
                            if temp_mask.sum() > self.min_area:
                                lowx = borders[0]
                                hix = borders[1]
                                lowy = borders[2]
                                hiy = borders[3]
                                # Addition caused by rules of a:b which expands to a<=x<b,
                                # so to include upper bound we have to add 1
                                temp_mask_reduced = resizer.shrink(temp_mask, [lowx, lowy], [hix, hiy], True)
                                temp_image_reduced = np.multiply(image[lowx:hix+1, lowy:hiy+1], temp_mask_reduced)
                                stains.append((temp_image_reduced, temp_mask_reduced, lowx, lowy))
                            temp_mask = np.zeros(mask.shape, dtype=mask.dtype)
        return stains

    def find_common_parts(self, manual_segmentation, manual_segmentation_stains, automatic_segmentation, image,
                          common_percentage=0.80):
        """
        Method segregating automatic segmentation results according to manual one.

        Parameters
        ----------
        manual_segmentation : np.array
            Manual segmentation mask
        manual_segmentation_stains : list
            Result of get_list_of_stains() form pimutils.mask.separator
        automatic_segmentation : np.array
            Automated segmentation mask
        image : np.array
            Image slice
        common_percentage

        Returns
        -------
        list, list
            Returns set of two list compatible with get_list_of_stains() results
        """
        tumor = []
        not_tumor = []
        temp_mask = np.zeros(automatic_segmentation.shape, dtype=automatic_segmentation.dtype)
        pixels = []  # List of neighbouring unchecked pixels as address tuples
        if automatic_segmentation.sum() != 0:
            for stain in manual_segmentation_stains:
                offset = stain[1].shape
                offset = (offset[0] - 1, offset[1] - 1)
                x_limit = stain[2]
                y_limit = stain[3]
                for x in range(x_limit, x_limit + offset[0], 1):
                    for y in range(y_limit, y_limit + offset[1], 1):
                        if automatic_segmentation[x, y] == 1:  # Got hit
                            # Copy address values
                            lowx = x  # Would be set to left border of image
                            lowy = y  # Would be set to top border of image
                            hix = x  # Would be set to right border of image
                            hiy = y  # Would be set to bottom border of image
                            borders = (lowx, hix, lowy, hiy)
                            # Activate in new automatic_segmentation
                            automatic_segmentation[x, y] = 0
                            temp_mask[lowx, lowy] = 1
                            # Add to list of pixels waiting for neighbourhood check
                            pixels.append((lowx, lowy))
                            while len(pixels) > 0:  # Check neighbours
                                automatic_segmentation, temp_mask, pixels, borders = self.check_neighbourhood(
                                    automatic_segmentation, temp_mask, pixels, borders)
                                pixels.pop(0)  # Remove checked pixel from list
                            m1, com, m2 = comparator.raw_compare(manual_segmentation, temp_mask)
                            if com / (com + m2) > common_percentage:
                                if temp_mask.sum() > self.min_area:
                                    lowx = borders[0]
                                    hix = borders[1]
                                    lowy = borders[2]
                                    hiy = borders[3]
                                    temp_mask_reduced = resizer.shrink(temp_mask, [lowx, lowy], [hix, hiy],
                                                                       True)
                                    temp_image_reduced = np.multiply(image[lowx:(hix + 1), lowy:(hiy + 1)],
                                                                     temp_mask_reduced)
                                    tumor.append((temp_image_reduced, temp_mask_reduced, lowx, lowy))
            if automatic_segmentation.sum() != 0:
                not_tumor = self.get_list_of_stains((image, automatic_segmentation))
        return tumor, not_tumor
