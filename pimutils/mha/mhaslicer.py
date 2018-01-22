from pimutils.mha import mhaIO
from pimutils.mha import mhaMath
import numpy as np


def prepare_training_pairs(file_name, discard_bg=10, axis=0):
    """
    Function generating pairs of image slice and its mask.

    Parameters
    ----------
    file_name : string
        Defines file name to be converted
    discard_bg : int
        Defines value of max value in image to be treated as valid slice, default 10
    axis : int
        Value defining in which axis slicing would take place, default 1

    Returns
    -------
    flair_pairs, t1_pairs, t1c_pairs, t2_pairs
        Lists of tuples containing image slice and corresponding mask
    """
    path_flair = "./data/raw/flair/"+file_name+".mha"
    path_t1 = "./data/raw/t1/" + file_name + ".mha"
    path_t1c = "./data/raw/t1c/" + file_name + ".mha"
    path_t2 = "./data/raw/t2/" + file_name + ".mha"
    path_desc = "./data/raw/more/" + file_name + ".mha"
    mha_flair = mhaIO.load_mha(path_flair)
    mha_t1 = mhaIO.load_mha(path_t1)
    mha_t1c = mhaIO.load_mha(path_t1c)
    mha_t2 = mhaIO.load_mha(path_t2)
    mha_desc = mhaIO.load_mha(path_desc)
    if mha_desc.shape != mha_flair.shape:
        exit(-1)
    if mha_desc.shape != mha_t1.shape:
        exit(-1)
    if mha_desc.shape != mha_t1c.shape:
        exit(-1)
    if mha_desc.shape != mha_t2.shape:
        exit(-1)
    desc_slices = mhaIO.get_all_slices(mha_desc, axis)
    print("Binearizing masks, please wait...")
    for i in range(desc_slices.__len__()):
        if desc_slices[i].max() > 0:
            desc_slices[i] = mhaMath.med_image_binearize(desc_slices[i])
    flair_slices = mhaIO.get_all_slices(mha_flair, axis)
    t1_slices = mhaIO.get_all_slices(mha_t1, axis)
    t1c_slices = mhaIO.get_all_slices(mha_t1c, axis)
    t2_slices = mhaIO.get_all_slices(mha_t2, axis)
    flair_pairs = []
    t1_pairs = []
    t1c_pairs = []
    t2_pairs = []
    for iterat in range(desc_slices.__len__()):
        flair_pairs.append((flair_slices[iterat], np.copy(desc_slices[iterat]).astype(desc_slices[iterat].dtype)))
        t1_pairs.append((t1_slices[iterat], np.copy(desc_slices[iterat]).astype(desc_slices[iterat].dtype)))
        t1c_pairs.append((t1c_slices[iterat], np.copy(desc_slices[iterat]).astype(desc_slices[iterat].dtype)))
        t2_pairs.append((t2_slices[iterat], np.copy(desc_slices[iterat]).astype(desc_slices[iterat].dtype)))
    # iterator = 0
    # print("Pairing FLAIR images, please wait...")
    # for mslice in mhaIO.get_all_slices(mha_flair, axis):
    #     if mslice.max() >= discard_bg:
    #         flair_pairs.append((mslice, np.copy(desc_slices[iterator]).astype(desc_slices[iterator].dtype)))
    #     iterator += 1
    # iterator = 0
    # print("Pairing T1 images, please wait...")
    # for mslice in mhaIO.get_all_slices(mha_t1, axis):
    #     if mslice.max() >= discard_bg:
    #         t1_pairs.append((mslice, np.copy(desc_slices[iterator]).astype(desc_slices[iterator].dtype)))
    #     iterator += 1
    # iterator = 0
    # print("Pairing T1C images, please wait...")
    # for mslice in mhaIO.get_all_slices(mha_t1c, axis):
    #     if mslice.max() >= discard_bg:
    #         t1c_pairs.append((mslice, np.copy(desc_slices[iterator]).astype(desc_slices[iterator].dtype)))
    #     iterator += 1
    # iterator = 0
    # print("Pairing T2 images, please wait...")
    # for mslice in mhaIO.get_all_slices(mha_t2, axis):
    #     if mslice.max() >= discard_bg:
    #         t2_pairs.append((mslice, np.copy(desc_slices[iterator]).astype(desc_slices[iterator].dtype)))
    #     iterator += 1
    return flair_pairs, t1_pairs, t1c_pairs, t2_pairs


def prepare_testing_pairs(file_name, patient):
    """
    Function generating pairs of image slice and its mask.

    Parameters
    ----------
    file_name : string
        Defines file name to be converted
    patient : string
        patient directory name

    Returns
    -------
    list of list of tuples
        Lists of tuples containing image slice and layer id
    """
    path_string = "./classify/structured/pat_"+patient.__str__()+"/"+file_name
    mha_file = mhaIO.load_mha(path_string)
    slices = []
    slices0 = []
    slices1 = []
    slices2 = []
    iterator = 0
    print("Pairing FLAIR images, please wait...")
    for mslice in mhaIO.get_all_slices(mha_file, 0):
        slices0.append((mslice, iterator))
        iterator += 1
    slices.append(slices0)
    iterator = 0
    for mslice in mhaIO.get_all_slices(mha_file, 1):
        slices1.append((mslice, iterator))
        iterator += 1
    slices.append(slices1)
    iterator = 0
    for mslice in mhaIO.get_all_slices(mha_file, 2):
        slices2.append((mslice, iterator))
        iterator += 1
    slices.append(slices2)
    return slices


def save_segmentation(segmentation, patient):
    mhaIO.save_mha(segmentation, "./classify/structured/pat_"+patient.__str__()+"/classification.mha")
