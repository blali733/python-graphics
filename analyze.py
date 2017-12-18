import sys  #for command line arguments
from imutils import imagemanager


class Analyze:
    def run(self, argv):
        print("I am the main now!")
        imageManager = imagemanager.ImageManager()
        image = imageManager.readImage('brain.jpg')
        threshold, image = imageManager.binearizeImage(image, 20)
        contours = imageManager.findContours(image)
        imageManager.contours2angdist(contours, image.shape[0]/2, image.shape[1]/2)
        imageManager.showImage(image, "title")


if __name__ == "__main__":
    app = Analyze()
    app.run(sys.argv)