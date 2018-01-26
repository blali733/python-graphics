import os
import shutil
import pathlib
from osutils import pathtools


class Sorter:
    def __init__(self):
        self.patient_dict = {}

    def main(self):
        pathlib.Path('./data/raw/flair').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/t1').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/t1c').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/t2').mkdir(parents=True, exist_ok=True)
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
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/flair/pat"+self.get_patient_id_from_dir(rootd).__str__()+".mha")
                    print("copied "+file+" to FLAIR")
                elif "T1." in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/t1/pat"+self.get_patient_id_from_dir(rootd).__str__()+".mha")
                    print("copied " + file + " to T1")
                elif "T1c" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/t1c/pat"+self.get_patient_id_from_dir(rootd).__str__()+".mha")
                    print("copied " + file + " to T1C")
                elif "T2" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/t2/pat"+self.get_patient_id_from_dir(rootd).__str__()+".mha")
                    print("copied " + file + " to T2")
                elif ".mha" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/more/pat"+self.get_patient_id_from_dir(rootd).__str__()+".mha")
                    print("copied " + file + " to MORE")
                else:
                    excludes.append(file)
        print(excludes)

    def get_patient_id_from_dir(self, path):
        try:
            id = self.patient_dict[pathtools.get_folder_name_from_path(path, -2)]
        except TypeError:
            id = 0
        return id
