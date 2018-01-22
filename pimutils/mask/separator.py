import numpy as np
from pimutils.mask import comparator
from pimutils import resizer

# TODO move pixel neighbourhood checking to another function, or at least analize feasibility of such solution


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
            List of tuples in form: nparray, nparray, int, int containing masked image fragment, mask fragment, x and y
            of left upper corner of fragment in whole image
        """
        stains = []  # List of results
        pixels = []  # List of neighbouring unchecked pixels as address tuples
        image = two_layer_image[0]
        mask = np.copy(two_layer_image[1]).astype(two_layer_image[1].dtype)
        temp_mask = np.zeros(mask.shape, dtype=mask.dtype)
        if mask.max() == 1:
            for y in range(mask.shape[0]-1):
                if mask[y, :].max() == 1:
                    for x in range(mask.shape[1] - 1):
                        if mask[y, x] == 1:  # Got hit
                            # Copy address values
                            lowx = x  # Would be set to left border of image
                            lowy = y  # Doubles as upper bound of image - scanning method makes it impossible to go higher
                            hix = x   # Would be set to right border of image
                            hiy = y   # Would be set to bottom border of image
                            # Activate in new mask
                            mask[y, x] = 0
                            temp_mask[lowy, lowx] = 1
                            # Add to list of pixels waiting for neighbourhood check
                            pixels.append((lowy, lowx))
                            while len(pixels) > 0:  # Check neighbours
                                ty = pixels[0][0]
                                tx = pixels[0][1]
                                # region Checking neighbours
                                # top
                                try:
                                    if mask[ty - 1, tx] == 1:
                                        temp_mask[ty - 1, tx] = 1
                                        pixels.append((ty - 1, tx))
                                        mask[ty - 1, tx] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # top - right
                                try:
                                    if mask[ty - 1, tx + 1] == 1:
                                        temp_mask[ty - 1, tx + 1] = 1
                                        pixels.append((ty - 1, tx + 1))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        mask[ty - 1, tx + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # right
                                try:
                                    if mask[ty, tx + 1] == 1:
                                        temp_mask[ty, tx + 1] = 1
                                        pixels.append((ty, tx + 1))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        mask[ty, tx + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom - right
                                try:
                                    if mask[ty + 1, tx + 1] == 1:
                                        temp_mask[ty + 1, tx + 1] = 1
                                        pixels.append((ty + 1, tx + 1))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        mask[ty + 1, tx + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom
                                try:
                                    if mask[ty + 1, tx] == 1:
                                        temp_mask[ty + 1, tx] = 1
                                        pixels.append((ty + 1, tx))
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        mask[ty + 1, tx] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom - left
                                try:
                                    if mask[ty + 1, tx - 1] == 1:
                                        temp_mask[ty + 1, tx - 1] = 1
                                        pixels.append((ty + 1, tx - 1))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        mask[ty + 1, tx - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # left
                                try:
                                    if mask[ty, tx - 1] == 1:
                                        temp_mask[ty, tx - 1] = 1
                                        pixels.append((ty, tx - 1))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        mask[ty, tx - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # top - left
                                try:
                                    if mask[ty - 1, tx - 1] == 1:
                                        temp_mask[ty - 1, tx - 1] = 1
                                        pixels.append((ty - 1, tx - 1))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        mask[ty - 1, tx - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # endregion
                                pixels.pop(0)  # Remove checked pixel from list
                            if temp_mask.sum() > self.min_area:
                                # Addition caused by rules of a:b which expands to a<=x<b,
                                # so to include upper bound we have to add 1
                                temp_mask_reduced = resizer.shrink(temp_mask, [lowx, lowy], [hix + 1, hiy + 1], True)  # temp_mask[lowy:(hiy+1), lowx:(hix+1)]
                                temp_image_reduced = np.multiply(image[lowy:(hiy+1), lowx:(hix+1)], temp_mask_reduced)
                                stains.append((temp_image_reduced, temp_mask_reduced, lowx, lowy))
                            temp_mask = np.zeros(mask.shape, dtype=mask.dtype)
        return stains

    def find_common_parts(self, manual_segmentation, manual_segmentation_stains, automatic_segmentation, image,
                          common_percentage=0.85):
        """

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
                m2full = stain[1].sum()
                offset = stain[1].shape
                x_limit = stain[2]
                y_limit = stain[3]
                for x in range(offset[1], x_limit, 1):
                    for y in range(offset[0], y_limit, 1):
                        if automatic_segmentation[y, x] == 1:  # Got hit
                            # Copy address values
                            lowx = x  # Would be set to left border of image
                            lowy = y  # Doubles as upper bound of image - scanning method makes it impossible to go higher
                            hix = x  # Would be set to right border of image
                            hiy = y  # Would be set to bottom border of image
                            # Activate in new automatic_segmentation
                            automatic_segmentation[y, x] = 0
                            temp_mask[lowy, lowx] = 1
                            # Add to list of pixels waiting for neighbourhood check
                            pixels.append((lowy, lowx))
                            while len(pixels) > 0:  # Check neighbours
                                # region Checking neighbours
                                ty = pixels[0][0]
                                tx = pixels[0][1]
                                # top
                                try:
                                    if automatic_segmentation[ty - 1, tx] == 1:
                                        temp_mask[ty - 1, tx] = 1
                                        pixels.append((ty - 1, tx))
                                        automatic_segmentation[ty - 1, tx] = 0
                                        if ty - 1 < lowy:
                                            lowy = ty-1
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # top - right
                                try:
                                    if automatic_segmentation[ty - 1, tx + 1] == 1:
                                        temp_mask[ty - 1, tx + 1] = 1
                                        pixels.append((ty - 1, tx + 1))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        if ty - 1 < lowy:
                                            lowy = ty - 1
                                        automatic_segmentation[ty - 1, tx + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # right
                                try:
                                    if automatic_segmentation[ty, tx + 1] == 1:
                                        temp_mask[ty, tx + 1] = 1
                                        pixels.append((ty, tx + 1))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        automatic_segmentation[ty, tx + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom - right
                                try:
                                    if automatic_segmentation[ty + 1, tx + 1] == 1:
                                        temp_mask[ty + 1, tx + 1] = 1
                                        pixels.append((ty + 1, tx + 1))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        automatic_segmentation[ty + 1, tx + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom
                                try:
                                    if automatic_segmentation[ty + 1, tx] == 1:
                                        temp_mask[ty + 1, tx] = 1
                                        pixels.append((ty + 1, tx))
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        automatic_segmentation[ty + 1, tx] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom - left
                                try:
                                    if automatic_segmentation[ty + 1, tx - 1] == 1:
                                        temp_mask[ty + 1, tx - 1] = 1
                                        pixels.append((ty + 1, tx - 1))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        automatic_segmentation[ty + 1, tx - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # left
                                try:
                                    if automatic_segmentation[ty, tx - 1] == 1:
                                        temp_mask[ty, tx - 1] = 1
                                        pixels.append((ty, tx - 1))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        automatic_segmentation[ty, tx - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # top - left
                                try:
                                    if automatic_segmentation[ty - 1, tx - 1] == 1:
                                        temp_mask[ty - 1, tx - 1] = 1
                                        pixels.append((ty - 1, tx - 1))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        if ty - 1 < lowy:
                                            lowy = ty-1
                                        automatic_segmentation[ty - 1, tx - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # endregion
                                pixels.pop(0)  # Remove checked pixel from list
                            m1, com, m2 = comparator.raw_compare(manual_segmentation, temp_mask)
                            if com / (com + m2) > common_percentage:
                                if temp_mask.sum() > self.min_area:
                                    temp_mask_reduced = resizer.shrink(temp_mask, [lowx, lowy], [hix + 1, hiy + 1], True)  # temp_mask[lowy:(hiy + 1), lowx:(hix + 1)]
                                    temp_image_reduced = np.multiply(image[lowy:(hiy + 1), lowx:(hix + 1)],
                                                                     temp_mask_reduced)
                                    tumor.append((temp_image_reduced, temp_mask_reduced, lowx, lowy))
                                    print("Tumor candidate accepted")
                                else:
                                    print("Tumor candidate dropped - low area")
                            else:
                                print("Tumor candidate dropped - to big overshoot: " + (com / (com + m2)).__str__(), com, m2)
            if automatic_segmentation.sum() != 0:
                not_tumor = self.get_list_of_stains((image, automatic_segmentation))
        else:
            print("empty")
        return tumor, not_tumor
