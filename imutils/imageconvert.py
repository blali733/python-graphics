from medpy.io import load


class ImageConvert:
    def main(self):
        i, h = load("../data/raw/img/657_2_1.img")
        print(h)
