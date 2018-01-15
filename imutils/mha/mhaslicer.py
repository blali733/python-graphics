import SimpleITK as sitk
import pathlib
import numpy as np


def prepare_trainig_pairs(file_name, discard_bg, axis=1):
    path_flair = "./data/raw/flair/"+file_name+".mha"
    path_t1 = "./data/raw/t1/" + file_name + ".mha"
    path_t1c = "./data/raw/t1c/" + file_name + ".mha"
    path_t2 = "./data/raw/t2/" + file_name + ".mha"
    path_desc = "./data/raw/more/" + file_name + ".mha"
    mha_flair = sitk.GetArrayFromImage(sitk.ReadImage(path_flair))
    mha_t1 = sitk.GetArrayFromImage(sitk.ReadImage(path_t1))
    mha_t1c = sitk.GetArrayFromImage(sitk.ReadImage(path_t1c))
    mha_t2 = sitk.GetArrayFromImage(sitk.ReadImage(path_t2))
    mha_desc = sitk.GetArrayFromImage(sitk.ReadImage(path_desc))
    if mha_desc.shape != mha_flair.shape:
        exit(-1)
    if mha_desc.shape != mha_t1.shape:
        exit(-1)
    if mha_desc.shape != mha_t1c.shape:
        exit(-1)
    if mha_desc.shape != mha_t2.shape:
        exit(-1)
    touch_dirs()
    desc_slices = slice(mha_desc, axis)
    iterator = 0
    for mslice in slice(mha_flair, axis):
        if mslice.max() >= discard_bg:
            sitk.WriteImage(sitk.GetImageFromArray([mslice, desc_slices[iterator]]),
                            "./data/parsed/flair/" + file_name + "_flair_" + iterator + ".mha")
        iterator += 1
    iterator = 0
    for mslice in slice(mha_t1, axis):
        if mslice.max() >= discard_bg:
            sitk.WriteImage(sitk.GetImageFromArray([mslice, desc_slices[iterator]]),
                            "./data/parsed/flair/" + file_name + "_t1_" + iterator + ".mha")
        iterator += 1
    iterator = 0
    for mslice in slice(mha_t1c, axis):
        if mslice.max() >= discard_bg:
            sitk.WriteImage(sitk.GetImageFromArray([mslice, desc_slices[iterator]]),
                            "./data/parsed/flair/" + file_name + "_t1c_" + iterator + ".mha")
        iterator += 1
    iterator = 0
    for mslice in slice(mha_t2, axis):
        if mslice.max() >= discard_bg:
            sitk.WriteImage(sitk.GetImageFromArray([mslice, desc_slices[iterator]]),
                            "./data/parsed/flair/" + file_name + "_t2_" + iterator + ".mha")
        iterator += 1


def touch_dirs():
    pathlib.Path('./data/parsed/flair').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1c').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t2').mkdir(parents=True, exist_ok=True)


def slice(image, axis):
    slices = []
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
