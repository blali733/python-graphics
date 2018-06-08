import os

from src.osutils import pathtools
from src.osutils.fileIO.directories import check_parsed_dirs
from src.tools.imageSorter import Sorter
from src.tools.mask import separator
from src.tools.mha import mhaSlicer
from src.tools.preparation.slices import parse_slices


def generate_list_of_patients():
    """
    Method responsible for generating list of patients to be analyzed.

    Returns
    -------
    list of tuples : (string, string, string, string, string)
        patient directory and file names.
    """
    patients_list = []
    flair_list = {}
    t1_list = {}
    t1c_list = {}
    t2_list = {}
    for rootd, subFolders, files in os.walk("./classify/structured"):
        for file in files:
            # flair_list[pathtools.get_folder_name_from_path(rootd, -1)] = file
            if "flair" in file:
                flair_list[pathtools.get_folder_name_from_path(rootd, -1)] = file
    #         elif "T1." in file:
    #             t1_list[pathtools.get_folder_name_from_path(rootd, -1)] = file
    #         elif "T1c" in file:
    #             t1c_list[pathtools.get_folder_name_from_path(rootd, -1)] = file
    #         elif "T2" in file:
    #             t2_list[pathtools.get_folder_name_from_path(rootd, -1)] = file
    for i in range(flair_list.__len__()):
        patients_list.append((i, flair_list["pat_" + i.__str__()]))
    #     patients_list.append((i, flair_list["pat_"+i.__str__()], t1_list["pat_"+i.__str__()], t1c_list["pat_"+i.__str__()], t2_list["pat_"+i.__str__()]))
    return patients_list


def prepare_data():
    """
    Method responsible for converting input data from mha files to learning sets.
    """
    answer = input("Do you want to prepare training images (y/N): ")
    if 'Y' in answer.capitalize():
        subapp = Sorter()
        subapp.main()
    answer = input("Do you want to prepare training image pairs (y/N): ")
    sep = separator.Separator(10)
    if 'Y' in answer.capitalize():
        flair_yes = 0
        # t1_yes = 0
        # t1c_yes = 0
        # t2_yes = 0
        flair_no = 0
        # t1_no = 0
        # t1c_no = 0
        # t2_no = 0
        yes_counters = (flair_yes)  #, t1_yes, t1c_yes, t2_yes)
        no_counters = (flair_no)  #, t1_no, t1c_no, t2_no)
        check_parsed_dirs()
        for root, subFolders, files in os.walk("./data/raw/flair"):
            for file in files:
                file_name_parts = file.split(".")
                print("Slicing file " + file_name_parts[0])
                # Axis 0
                flair = mhaSlicer.prepare_training_pairs(file_name_parts[0], axis=0)
                slices_tuple = (flair)
                yes_counters, no_counters = parse_slices(slices_tuple, yes_counters, no_counters, sep, 0)
                # Axis 1
                flair = mhaSlicer.prepare_training_pairs(file_name_parts[0], axis=1)
                slices_tuple = (flair)
                yes_counters, no_counters = parse_slices(slices_tuple, yes_counters, no_counters, sep, 1)
                # Axis 2
                flair = mhaSlicer.prepare_training_pairs(file_name_parts[0], axis=2)
                slices_tuple = (flair)
                yes_counters, no_counters = parse_slices(slices_tuple, yes_counters, no_counters, sep, 2)
        print("Flair: tumor - " + yes_counters.__str__() + "; not - " + no_counters.__str__())
        # print("T1: tumor - " + yes_counters[1].__str__() + "; not - " + no_counters[1].__str__())
        # print("T1c: tumor - " + yes_counters[2].__str__() + "; not - " + no_counters[2].__str__())
        # print("T2: tumor - " + yes_counters[3].__str__() + "; not - " + no_counters[3].__str__())
