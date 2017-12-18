import sys  #for command line arguments
from imutils import imagemanager
from imutils import imagecrop
import cv2


class Analyze:
    def run(self, argv):
        print("I am the main now!")
        imageManager = imagemanager.ImageManager()
        imageCrop = imagecrop.ImageCrop()
        image = imageManager.readImage('brain.jpg')
        threshold, imagebin = imageManager.binearizeImage(image, 20)
        cv2.imshow("rrr", imagebin)
        contours = imageManager.findContours(imagebin)
        newContours = imageManager.contours2angdist(contours, image.shape[0]/2, image.shape[1]/2)
        finContours = imageManager.choosePointsForExpectingContour(newContours, 300)
        image2 = imageCrop.excludeBackground(finContours,image)
        imageManager.showImage(image, "title")


if __name__ == "__main__":
    app = Analyze()
    app.run(sys.argv)