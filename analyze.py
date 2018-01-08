import sys  # for command line arguments
from imutils import imageconvert
from imutils import imagemanager
from imutils import imagecrop


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
                pass
            elif mode == 2:
                pass
            elif mode == 3:
                pass
            elif mode == 4:
                pass


# imageManager = imagemanager.ImageManager()
#         imageCrop = imagecrop.ImageCrop()
#         image = imageManager.readImage('brain.jpg')
#         threshold, imagebin = imageManager.binearizeImage(image, 25)
#         # cv2.imshow("rrr", imagebin)
#         contours = imageManager.findContours(imagebin)
#         newContours = imageManager.contours2angdist(contours, image.shape[0]/2, image.shape[1]/2)
#         finContours = imageManager.choosePointsForExpectingContour(newContours, 100, 7.5)
#         image2 = imageCrop.excludeBackground(finContours,image)
#         threshold, image2 = imageManager.binearizeImage(image2, 180)
#         imageManager.showImage(image2, "title")

if __name__ == "__main__":
    app = Analyze()
    app.run(sys.argv)
