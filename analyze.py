import sys  #for command line arguments
from imutils import imagemanager


class Analyze:
    def run(self, argv):
        print("I am the main now!")


if __name__ == "__main__":
    app = Analyze()
    app.run(sys.argv)