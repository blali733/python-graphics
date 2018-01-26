import os
import pathlib
import shutil

from osutils import pathtools


def create_patient_dir(patient):
    try:
        pathlib.Path("./classify/structured/"+patient).mkdir(parents=True)
    except OSError as exc:
        if exc.errno == 17:
            shutil.rmtree("./classify/structured/"+patient, ignore_errors=True)
            pathlib.Path("./classify/structured/" + patient).mkdir(parents=True)
        else:
            raise


def check_classify_input_dir():
    shutil.rmtree("./classify/structured/", ignore_errors=True)
    pathlib.Path("./classify/structured/").mkdir(parents=True)
    patient_dict = {}
    patient_id = 0
    for root, subFolders, files in os.walk('./classify/raw'):
        for folder in subFolders:
            if "brats" in folder:
                create_patient_dir("pat_" + patient_id.__str__())
                patient_dict[folder] = patient_id
                patient_id += 1
        for file in files:
            if ".txt" in file:
                os.remove(os.path.join(root, file))
            elif ".mha" in file:
                try:
                    id = patient_dict[pathtools.get_folder_name_from_path(root, -2)]
                    shutil.copy2(os.path.join(root, file), "./classify/structured/" + id.__str__() + "/" + file)
                except TypeError:
                    print("Unknown patient file!")
    pass


def check_parsed_dirs():
    pathlib.Path('./data/parsed/flair').mkdir(parents=True, exist_ok=True)
    shutil.rmtree('./data/parsed/flair/tumor', ignore_errors=True)
    shutil.rmtree('./data/parsed/flair/not', ignore_errors=True)
    pathlib.Path('./data/parsed/flair/tumor').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/flair/not').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1').mkdir(parents=True, exist_ok=True)
    shutil.rmtree('./data/parsed/t1/tumor', ignore_errors=True)
    shutil.rmtree('./data/parsed/t1/not', ignore_errors=True)
    pathlib.Path('./data/parsed/t1/tumor').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1/not').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1c').mkdir(parents=True, exist_ok=True)
    shutil.rmtree('./data/parsed/t1c/tumor', ignore_errors=True)
    shutil.rmtree('./data/parsed/t1c/not', ignore_errors=True)
    pathlib.Path('./data/parsed/t1c/tumor').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t1c/not').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t2').mkdir(parents=True, exist_ok=True)
    shutil.rmtree('./data/parsed/t2/tumor', ignore_errors=True)
    shutil.rmtree('./data/parsed/t2/not', ignore_errors=True)
    pathlib.Path('./data/parsed/t2/tumor').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./data/parsed/t2/not').mkdir(parents=True, exist_ok=True)