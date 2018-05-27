import os
import shutil
import pathlib
from src.osutils import pathtools


class Sorter:
    """
    Class containing logic of training data sorting.
    """
    def __init__(self):
        """
        Initializer of Sorter class, reserves class variable for patient dictionary.
        """
        self.patient_dict = {}

    def main(self):
        """
        Method responsible for dividing content of brats2015 training set into proper directories.
        """
        pathlib.Path('./data/raw/flair').mkdir(parents=True, exist_ok=True)
        # pathlib.Path('./data/raw/t1').mkdir(parents=True, exist_ok=True)
        # pathlib.Path('./data/raw/t1c').mkdir(parents=True, exist_ok=True)
        # pathlib.Path('./data/raw/t2').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/more').mkdir(parents=True, exist_ok=True)
        root = input("Please provide path to BRATS2015 training data directory: ")
        patient_id = 0
        excludes = []
        for rootd, subFolders, files in os.walk(root):
            for folder in subFolders:
                if "brats" in folder:
                    patient_id += 1
                    self.patient_dict[folder] = patient_id
            for file in files:
                if ".txt" in file:
                    os.remove(os.path.join(rootd, file))
                elif "Flair" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/flair/pat" +
                                 self.patient_dict[pathtools.get_folder_name_from_path(rootd, -2)].__str__() + ".mha")
                    print("copied "+file+" to FLAIR")
                elif "T1." in file:
                    pass
                    # shutil.copy2(os.path.join(rootd, file), "./data/raw/t1/pat" +
                    #              pathtools.get_folder_name_from_path(rootd, -2).__str__() + ".mha")
                    # print("copied " + file + " to T1")
                elif "T1c" in file:
                    pass
                    # shutil.copy2(os.path.join(rootd, file), "./data/raw/t1c/pat" +
                    #              pathtools.get_folder_name_from_path(rootd, -2).__str__() + ".mha")
                    # print("copied " + file + " to T1C")
                elif "T2" in file:
                    pass
                    # shutil.copy2(os.path.join(rootd, file), "./data/raw/t2/pat" +
                    #              pathtools.get_folder_name_from_path(rootd, -2).__str__() + ".mha")
                    # print("copied " + file + " to T2")
                elif ".mha" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/more/pat" +
                                 self.patient_dict[pathtools.get_folder_name_from_path(rootd, -2)].__str__() + ".mha")
                    print("copied " + file + " to MORE")
                else:
                    excludes.append(file)
        print(excludes)
