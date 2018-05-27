import matplotlib
# set the matplotlib backend so figures can be saved in the background
matplotlib.use("Agg")
from src.tools.mha import mhaSlicer
from src.nnutils import test
from src.nnutils import teach
from src.osutils.fileIO.directories import check_classify_input_dir
from src.tools.preparation.file2mem import generate_list_of_patients, prepare_data
from src.tools.preparation.slices import generate_tumor_map


# Kept as reference for checking execution time:
# t = timeit.Timer(functools.partial(sep.get_list_of_stains, flair[100]))
# print(t.timeit(1))


class Analyze:
    """
    Analyzer class - control unit of application.
    """
    def __init__(self):
        """
        Initializer of Analyze class, creates variables used to store classifier parameters.
        """
        self.classifier_class = None
        self.classifier_load_status = False
        self.classifier_name = ""

    def run(self):
        """
        Main loop of tumor analyzer script.
        """
        fuse = 1
        while fuse == 1:
            self.menu()
            # t = timeit.Timer(self.prepare_data)
            # print(t.timeit(1))
            try:
                mode = int(input('Your choice: '))
            except ValueError:
                print("Not a number!")
                mode = -1
            if mode == 0:
                exit(0)
            elif mode == 1:  # Prepare input
                prepare_data()
            elif mode == 2:  # Teaching
                self.teach_classifier()
            elif mode == 3:  # Load classifier
                self.load_classifier()
            elif mode == 4:  # Classify images
                self.classify_images()

    # region Menu options
    def teach_classifier(self):
        """
        Method responsible for teaching classifier basing on learning sets.
        """
        name = input('Please provide model name: ')
        classifier_name = input('Please provide base model name (LeNet, VGG, SimpleVGG): ')
        test = input('Do you want to use only 10 epochs instead of 25? (y/N) ')
        if test.capitalize() == 'Y':
            teacher = teach.Teacher(epochs=10, model_name=classifier_name.upper())
            teacher.teach(name)
        else:
            teacher = teach.Teacher(model_name=classifier_name.upper())
            teacher.teach(name)

    def load_classifier(self):
        """
        Method responsible for loading saved classifier.
        """
        name = input('Please provide model name:')
        try:
            self.classifier_class = test.TestClassification(name)
            self.classifier_load_status = True
            self.classifier_name = name
        except NotADirectoryError:
            print("Unable to load classifier with name \""+name+"\" - directory does not exist.")
        except FileNotFoundError:
            print("Unable to load classifier with name \"" + name + "\" - at least one file does not exist.")

    def classify_images(self):
        """
        Method responsible for initiating image classification loop.
        """
        if self.classifier_load_status == 0:
            print("Load any classifier first.")
            return
        else:
            print("This would classify ALL images in ./classify/structured directory.")
            answer = input("Do you want to repopulate from classify/raw, this would erase all data? (y/N): ")
            if 'Y' in answer.capitalize():
                check_classify_input_dir()
            patients_list = generate_list_of_patients()
            for patient in patients_list:
                flair_slices = mhaSlicer.prepare_testing_pairs(patient[1], patient[0])
                # t1_slices = mhaSlicer.prepare_testing_pairs(patient[2], patient[0])
                # t1c_slices = mhaSlicer.prepare_testing_pairs(patient[3], patient[0])
                # t2_slices = mhaSlicer.prepare_testing_pairs(patient[4], patient[0])
                segmentation = generate_tumor_map(self.classifier_class,
                                                  (flair_slices))  # , t1_slices, t1c_slices, t2_slices))
                mhaSlicer.save_segmentation(segmentation, patient[0])
    # endregion

    def menu(self):
        """
        Method responsible for displaying main menu.
        """
        if self.classifier_load_status:
            print("Classifier " + self.classifier_name + " is LOADED")
        else:
            print("Classifier is NOT LOADED")
        print()
        print("Please select mode:")
        print("1 - prepare input data")
        print("2 - use prepared data as learning set")
        print("3 - load classifier data")
        print("4 - prepare and classify image")
        print("0 - exit")
        print()


if __name__ == "__main__":
    app = Analyze()
    app.run()
