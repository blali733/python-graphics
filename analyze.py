import functools
import pathlib
import sys  # for command line arguments
import os
import timeit
from pimutils.segmentation import segment as seg
from pimutils.mask import separator
from pimutils.mha import mhaslicer
from imageSorter import Sorter
from osutils import adfIO


class Analyze:
    @staticmethod
    def menu(isNNLoaded):
        if isNNLoaded == 0:
            print("Classifier is NOT LOADED")
        else:
            print("Classifier is LOADED")
        print()
        print("Please select mode:")
        print("1 - prepare input data")
        print("2 - use prepared data as learning set")
        print("3 - load classifier data")
        print("4 - prepare and classify image")
        print("0 - exit")
        print()

    def run(self, argv):
        fuse = 1
        nNLoadStatus = 0
        while fuse == 1:
            self.menu(nNLoadStatus)
            try:
                mode = int(input('Your choice:'))
            except ValueError:
                print("Not a number!")
                mode = -1
            if mode == 0:
                exit(0)
            elif mode == 1:
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
                                print("Slicing file "+file_name_parts[0])
                                flair, t1, t1c, t2 = mhaslicer.prepare_training_pairs(file_name_parts[0])
                                # t = timeit.Timer(functools.partial(sep.get_list_of_stains, flair[0]))
                                # print(t.timeit(1))
                                # t = timeit.Timer(functools.partial(sep.get_list_of_stains, flair[50]))
                                # print(t.timeit(1))
                                # t = timeit.Timer(functools.partial(sep.get_list_of_stains, flair[100]))
                                # print(t.timeit(1))
                                print("Dismantling FLAIR")
                                for imTuple in flair:
                                    ret_list = sep.get_list_of_stains(imTuple)
                                    for ret_tuple in ret_list:
                                        adfIO.save(ret_tuple[0], './data/parsed/flair/tumor/'+flair_no.__str__())
                                        flair_no += 1
                                print("Dismantling T1")
                                for imTuple in t1:
                                    ret_list = sep.get_list_of_stains(imTuple)
                                    for ret_tuple in ret_list:
                                        adfIO.save(ret_tuple[0], './data/parsed/t1/tumor/'+t1_no.__str__())
                                        t1_no += 1
                                print("Dismantling T1C")
                                for imTuple in t1c:
                                    ret_list = sep.get_list_of_stains(imTuple)
                                    for ret_tuple in ret_list:
                                        adfIO.save(ret_tuple[0], './data/parsed/t1c/tumor/'+t1c_no.__str__())
                                        t1c_no += 1
                                print("Dismantling T2")
                                for imTuple in t2:
                                    ret_list = sep.get_list_of_stains(imTuple)
                                    for ret_tuple in ret_list:
                                        adfIO.save(ret_tuple[0], './data/parsed/t2/tumor/'+t2_no.__str__())
                                        t2_no += 1
                                print("done")
            elif mode == 2:
                pass
            elif mode == 3:
                pass
            elif mode == 4:
                pass

    def check_parsed_dirs(self):
        pathlib.Path('./data/parsed/flair').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/flair/tumor').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/flair/not').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t1').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t1/tumor').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t1/not').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t1c').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t1c/tumor').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t1c/not').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t2').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t2/tumor').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/parsed/t2/not').mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    app = Analyze()
    app.run(sys.argv)
