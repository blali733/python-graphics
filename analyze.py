import sys  # for command line arguments
import os
from imutils import imageconvert
from imutils import imagemanager
from imutils import imagecrop
from imutils.mha import mhaslicer
from imageSorter import Sorter


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
                if 'y' in test:
                    subapp = Sorter()
                    subapp.main()
                test = input("Do you want to prepare training image pairs (y/N): ")
                if 'y' in test:
                    for root, subFolders, files in os.walk("./data/raw/flair"):
                        for file in files:
                            file_name_parts = file.split(".")
                            print("Slicing file "+file_name_parts[0])
                            mhaslicer.prepare_training_pairs(file_name_parts[0], 10)
                            print("done")
                imc = imageconvert.ImageConvert()
                imc.main()
            elif mode == 2:
                pass
            elif mode == 3:
                pass
            elif mode == 4:
                pass


if __name__ == "__main__":
    app = Analyze()
    app.run(sys.argv)
