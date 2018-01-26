import SimpleITK as sitk
import numpy as np


def load_mha(path):
    return sitk.GetArrayFromImage(sitk.ReadImage(path)).astype(np.int16)


def save_mha(array_of_layers, path):
    sitk.WriteImage(sitk.GetImageFromArray(array_of_layers), path)
