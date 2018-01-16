import pathlib
from imutils.mha import mhaIO
import numpy as np


def prepare_training_pairs(file_name, discard_bg, axis=1):
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
    touch_dirs()
    desc_slices = mhaIO.get_all_slices(mha_desc, axis)
    iterator = 0
    for mslice in mhaIO.get_all_slices(mha_flair, axis):
        if mslice.max() >= discard_bg:
            mhaIO.save_mha([mslice, desc_slices[iterator]],
                           "./data/parsed/flair/" + file_name + "_flair_" + iterator.__str__() + ".mha")
        iterator += 1
    iterator = 0
    for mslice in mhaIO.get_all_slices(mha_t1, axis):
        if mslice.max() >= discard_bg:
            mhaIO.save_mha([mslice, desc_slices[iterator]],
                           "./data/parsed/t1/" + file_name + "_t1_" + iterator.__str__() + ".mha")
        iterator += 1
    iterator = 0
    for mslice in mhaIO.get_all_slices(mha_t1c, axis):
        if mslice.max() >= discard_bg:
            mhaIO.save_mha([mslice, desc_slices[iterator]],
                           "./data/parsed/t1c/" + file_name + "_t1c_" + iterator.__str__() + ".mha")
        iterator += 1
    iterator = 0
    for mslice in mhaIO.get_all_slices(mha_t2, axis):
        if mslice.max() >= discard_bg:
            mhaIO.save_mha([mslice, desc_slices[iterator]],
                           "./data/parsed/t2/" + file_name + "_t2_" + iterator.__str__() + ".mha")
        iterator += 1


def touch_dirs():
    pathlib.Path('./data/parsed/flair').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1c').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t2').mkdir(parents=True, exist_ok=True)
