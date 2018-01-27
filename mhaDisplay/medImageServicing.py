import numpy as np
import SimpleITK as sitk
import matplotlib as mpl
import matplotlib.pyplot as plt
import pathlib
import os


class Plotter:
    """
    Hermetic class containing logic required to represent mha images as layers in image viewer.
    """
    def __init__(self):
        mpl.rcParams['toolbar'] = 'None'
        self.image_abs = None
        self.image_rel = None
        self.image_shape = None
        self.mask = None
        self.name = None
        self.mask_cutoff = 0
        self.axis = 0
        self.layer = 0
        self.relative = 0
        self.overlay = 0
        self.image_max = 0

    def set_image(self, image_path):
        image = sitk.GetArrayFromImage(sitk.ReadImage(image_path))
        if os.name == "nt":
            self.name = image_path.split('\\')[-1]
        else:
            self.name = image_path.split('/')[-1]
        self.image_max = image.max()
        self.axis = 0
        self.layer = 0
        self.image_shape = image.shape
        self.image_abs = []
        self.image_abs.append(self.get_all_slices(image, 0))
        self.image_abs.append(self.get_all_slices(image, 1))
        self.image_abs.append(self.get_all_slices(image, 2))
        self.image_rel = []
        self.image_rel.append(self.get_all_slices(image, 0, False))
        self.image_rel.append(self.get_all_slices(image, 1, False))
        self.image_rel.append(self.get_all_slices(image, 2, False))
        self.redraw()

    def set_mask(self, image_path):
        image = sitk.GetArrayFromImage(sitk.ReadImage(image_path))
        if self.image_shape != image.shape:
            raise TypeError("Mask and image size mismatch!")
        self.overlay = 1
        self.mask = []
        self.mask_cutoff = 0
        self.mask.append(self.get_all_slices(image, 0, convert=False))
        self.mask.append(self.get_all_slices(image, 1, convert=False))
        self.mask.append(self.get_all_slices(image, 2, convert=False))
        self.redraw()

    def unset_mask(self):
        self.mask = None
        self.overlay = 0
        self.redraw()
        
    def redraw(self):
        if self.overlay == 0:
            if self.relative == 1:
                image = self.image_rel[self.axis][self.layer]
            else:
                image = self.image_abs[self.axis][self.layer]
            result = np.stack([image, image, image], axis=2)
            plt.imshow(result)
        else:
            mask = self.binearize(self.mask[self.axis][self.layer], self.mask_cutoff)
            if self.relative == 1:
                image = self.image_rel[self.axis][self.layer]
            else:
                image = self.image_abs[self.axis][self.layer]
            masked_image = np.multiply(image, mask)
            result = np.stack([image, masked_image, masked_image], axis=2)
            plt.imshow(result)
        text = self.name + " axis: " + self.axis.__str__() + " layer: " + self.layer.__str__()
        plt.title(text)
        plt.pause(0.0001)

    def get_all_slices(self, image, axis, absolute_conversion=True, convert=True):
        slices = []
        if convert:
            if absolute_conversion:
                variant = True
            else:
                variant = False
            if axis == 0:
                for i in range(image.shape[0]):
                    slices.append(self.int_2_float(image[i, :, :], variant))
            elif axis == 1:
                for i in range(image.shape[1]):
                    slices.append(self.int_2_float(image[:, i, :], variant))
            elif axis == 2:
                for i in range(image.shape[2]):
                    slices.append(self.int_2_float(image[:, :, i], variant))
        else:
            if axis == 0:
                for i in range(image.shape[0]):
                    slices.append(image[i, :, :])
            elif axis == 1:
                for i in range(image.shape[1]):
                    slices.append(image[:, i, :])
            elif axis == 2:
                for i in range(image.shape[2]):
                    slices.append(image[:, :, i])
        return slices

    def toggle_overlay(self):
        if self.mask is not None:
            self.overlay ^= 1
            self.redraw()

    def toggle_relativity(self):
        self.relative ^= 1
        self.redraw()

    def next_axis(self):
        self.axis += 1
        self.axis %= 3
        self.layer = 0
        self.redraw()
        
    def previous_axis(self):
        self.axis -= 1
        self.axis %= 3
        self.layer = 0
        self.redraw()

    def next_layer(self, offset=1):
        if self.layer + offset < self.image_shape[self.axis]-1:
            self.layer += offset
        else:
            self.layer = self.image_shape[self.axis]-1
        self.redraw()

    def prev_layer(self, offset=1):
        if self.layer - offset > 0:
            self.layer -= offset
        else:
            self.layer = 0
        self.redraw()

    def int_2_float(self, image_slice, absolute=True):
        """
        Converts any np.array into float format compatible with images.

        Parameters
        ----------
        image_slice : np.array
            Numpy array representing image
        absolute : bool
            Defines if scaling value should be taken as max of loaded image, or as local maximum of slice.

        Returns
        -------
        np.array
            normalized image.
        """
        if absolute:
            max_val = max(self.image_max, 1)
        else:
            max_val = image_slice.max()
            max_val = max(max_val, 1)
        val = 1 / max_val
        temp = image_slice.astype(np.float).copy()
        temp *= val  # Legends say that division is longer operation.
        return temp

    def binearize(self, med_image_slice, level=0):
        """
        Function binearizing numpy arrays

        Parameters
        ----------
        med_image_slice : np.array
            image to be binearized
        level : int
            level at which binearization would be performed; default 0

        Returns
        -------
        np.array
            binearized image as np.array
        """
        level = level + 0.5
        return (med_image_slice > level) * 1

    def get_size(self, axis):
        return self.image_shape[axis]

    def med_2_csv(self):
        pathlib.Path('./data/raw/csv').mkdir(parents=True, exist_ok=True)
        name = self.name + '_' + self.axis.__str__() + '_' + self.layer.__str__()
        file = open("./data/raw/csv/" + name + ".csv", "w")
        if self.relative == 1:
            image_slice = self.image_rel[self.axis][self.layer]
        else:
            image_slice = self.image_abs[self.axis][self.layer]
        for x in range(self.image_shape[0]):
            for y in range(self.image_shape[1]):
                file.write(image_slice[x, y].__str__()+"; ")
            file.write("\n")
        file.close()

    def get_info(self):
        print("Dimensions of file:", self.image_shape)
