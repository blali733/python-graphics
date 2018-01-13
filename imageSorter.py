import os
import sys
import shutil
import pathlib


class Sorter:
    def main(self):
        pathlib.Path('./data/raw/flair').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/t1').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/t1c').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/t2').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./data/raw/3more').mkdir(parents=True, exist_ok=True)
        root = input("Please provide path to input files directory: ")
        for rootd, subFolders, files in os.walk(root):
            for file in files:
                if ".txt" in file:
                    os.remove(os.path.join(rootd,file))
                if "Flair" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/flair")
                    print("copied "+file+" to FLAIR")
                if "T1." in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/t1")
                    print("copied " + file + " to T1")
                if "T1c" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/t1c")
                    print("copied " + file + " to T1C")
                if "T2" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/t2")
                    print("copied " + file + " to T2")
                if "more" in file:
                    shutil.copy2(os.path.join(rootd, file), "./data/raw/more")
                    print("copied " + file + " to MORE")


if __name__ == "__main__":
    app = Sorter()
    app.main()
