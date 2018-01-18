import numpy as np


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
            List of arrays in form: nparray, nparray, int, int containing masked image fragment, mask fragment, x and y
            of left upper corner of fragment in whole image
        """
        stains = []  # List of results
        pixels = []  # List of neighbouring unchecked pixels as address tuples
        image = two_layer_image[0]
        mask = two_layer_image[1]
        temp_mask = np.zeros(mask.shape)
        if mask.max() == 1:
            for x in range(mask.shape[0]-1):
                if mask[x, :].max() == 1:
                    for y in range(mask.shape[1] - 1):
                        if mask[x, y] == 1:  # Got hit
                            # Copy address values
                            lowx = x  # Would be set to left border of image
                            lowy = y  # Doubles as upper bound of image - scanning method makes it impossible to go higher
                            hix = x   # Would be set to right border of image
                            hiy = y   # Would be set to bottom border of image
                            # Activate in new mask
                            mask[x, y] = 0
                            temp_mask[lowx, lowy] = 1
                            # Add to list of pixels waiting for neighbourhood check
                            pixels.append((lowx, lowy))
                            while len(pixels) > 0:  # Check neighbours
                                tx = pixels[0][0]
                                ty = pixels[0][1]
                                # top
                                try:
                                    if mask[tx, ty - 1] == 1:
                                        temp_mask[tx, ty - 1] = 1
                                        pixels.append((tx, ty - 1))
                                        # mask[tx, ty - 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # right
                                try:
                                    if mask[tx + 1, ty] == 1:
                                        temp_mask[tx + 1, ty] = 1
                                        pixels.append((tx + 1, ty))
                                        if tx + 1 > hix:
                                            hix = tx + 1
                                        mask[tx + 1, ty] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # bottom
                                try:
                                    if mask[tx, ty + 1] == 1:
                                        temp_mask[tx, ty + 1] = 1
                                        pixels.append((tx, ty + 1))
                                        if ty + 1 > hiy:
                                            hiy = ty + 1
                                        mask[tx, ty + 1] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                # left
                                try:
                                    if mask[tx - 1, ty] == 1:
                                        temp_mask[tx - 1, ty] = 1
                                        pixels.append((tx - 1, ty))
                                        if tx - 1 < lowx:
                                            lowx = tx - 1
                                        mask[tx - 1, ty] = 0
                                except IndexError:  # In case of addressing pixel not in range
                                    pass
                                pixels.pop(0)  # Remove checked pixel from list
                            if temp_mask.sum() > self.min_area:
                                # Addition caused by rules of a:b which expands to a<=x<b,
                                # so to include upper bound we have to add 1
                                temp_mask_reduced = temp_mask[lowx:(hix+1), lowy:(hiy+1)]
                                temp_image_reduced = np.multiply(image[lowx:(hix+1), lowy:(hiy+1)], temp_mask_reduced)
                                stains.append((temp_image_reduced, temp_mask_reduced, lowx, lowy))
                            temp_mask = np.zeros(mask.shape)
        return stains
