import SimpleITK as sitk
import numpy as np


def load_mha(path):
    """
    Method loads mha file as np.array of type Int16

    Parameters
    ----------
    path : string
        Path to mha file

    Returns
    -------
    np.array
        Mha file as 3 dimensional numpy array of type Int16
    """
    return sitk.GetArrayFromImage(sitk.ReadImage(path)).astype(np.int16)


def save_mha(array_of_layers, path):
    """
    Method saves np.array to mha file

    Parameters
    ----------
    array_of_layers : np.array
        3d numpy array containing image to be saved
    path : string
        Path to output mha file.
    """
    sitk.WriteImage(sitk.GetImageFromArray(array_of_layers), path)
