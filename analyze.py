import functools
import pathlib
import sys  # for command line arguments
import os
import timeit
import shutil
from pimutils.segmentation import segment as seg
from pimutils.mask import separator
from pimutils.mha import mhaslicer
from imageSorter import Sorter
from osutils import adfIO
from nnutils import teach, test

# Kept as reference for checking execution time:
# t = timeit.Timer(functools.partial(sep.get_list_of_stains, flair[100]))
# print(t.timeit(1))


class Analyze:
    def __init__(self):
        self.classifier_load_status = False
        self.classifier_name = ""

    def run(self):
        fuse = 1
        while fuse == 1:
            self.menu()
            try:
                mode = int(input('Your choice:'))
            except ValueError:
                print("Not a number!")
                mode = -1
            if mode == 0:
                exit(0)
            elif mode == 1:  # Prepare input
                self.prepare_data()
            elif mode == 2:  # Teaching
                self.teach_classifier()
            elif mode == 3:  # Load classifier
                self.load_classifier()
            elif mode == 4:  # Classify images
                self.classify_images()

    # <editor-fold desc="Menu options">
    def prepare_data(self):
        """
        Method responsible for converting input data from mha files to learning sets.
        """
        test = input("Do you want to prepare training images (y/N): ")
        if 'Y' in test.capitalize():
            subapp = Sorter()
            subapp.main()
        test = input("Do you want to prepare training image pairs (y/N): ")
        sep = separator.Separator(10)
        if 'Y' in test.capitalize():
            flair_no = 0
            t1_no = 0
            t1c_no = 0
            t2_no = 0
            self.check_parsed_dirs()
            for root, subFolders, files in os.walk("./data/raw/flair"):
                for file in files:
                    file_name_parts = file.split(".")
                    if file_name_parts[0] == 'pat1':
                        print("Slicing file " + file_name_parts[0])
                        flair, t1, t1c, t2 = mhaslicer.prepare_training_pairs(file_name_parts[0])
                        print("Dismantling FLAIR")
                        for imTuple in flair:
                            ret_list = sep.get_list_of_stains(imTuple)
                            for ret_tuple in ret_list:
                                adfIO.save(ret_tuple[0], './data/parsed/flair/tumor/' + flair_no.__str__())
                                flair_no += 1
                        print("Dismantling T1")
                        for imTuple in t1:
                            ret_list = sep.get_list_of_stains(imTuple)
                            for ret_tuple in ret_list:
                                adfIO.save(ret_tuple[0], './data/parsed/t1/tumor/' + t1_no.__str__())
                                t1_no += 1
                        print("Dismantling T1C")
                        for imTuple in t1c:
                            ret_list = sep.get_list_of_stains(imTuple)
                            for ret_tuple in ret_list:
                                adfIO.save(ret_tuple[0], './data/parsed/t1c/tumor/' + t1c_no.__str__())
                                t1c_no += 1
                        print("Dismantling T2")
                        for imTuple in t2:
                            ret_list = sep.get_list_of_stains(imTuple)
                            for ret_tuple in ret_list:
                                adfIO.save(ret_tuple[0], './data/parsed/t2/tumor/' + t2_no.__str__())
                                t2_no += 1
                        print("done")

    def teach_classifier(self):
        """
        Method responsible for teaching classifier basing on learning sets.
        """
        pass

    def load_classifier(self):
        """
        Method responsible for loading saved classifier.
        """
        pass

    def classify_images(self):
        """
        Method responsible for initiating image classification loop.
        """
        if self.classifier_load_status == 0:
            print("Load any classifier first.")
            return
        else:
            pass
    # </editor-fold>

    # <editor-fold desc="Static functions">
    @staticmethod
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

    def menu(self):
        if is_classifier_loaded:
            print("Classifier is NOT LOADED")
        else:
            print("Classifier "+classifier_name+" is LOADED")
        print()
        print("Please select mode:")
        print("1 - prepare input data")
        print("2 - use prepared data as learning set")
        print("3 - load classifier data")
        print("4 - prepare and classify image")
        print("0 - exit")
        print()
    # </editor-fold>


if __name__ == "__main__":
    app = Analyze()
    app.run()
