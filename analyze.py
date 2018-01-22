import matplotlib
# set the matplotlib backend so figures can be saved in the background
matplotlib.use("Agg")
import functools
import pathlib
import sys  # for command line arguments
import os
import timeit
import shutil
from pimutils.segmentation import segment as seg
from pimutils.mask import separator, mirrorMask, recreate
from pimutils.mha import mhaslicer
from pimutils import resizer
from imageSorter import Sorter
from osutils import adfIO, pathtools
from nnutils import teach, test
import numpy as np

# Kept as reference for checking execution time:
# t = timeit.Timer(functools.partial(sep.get_list_of_stains, flair[100]))
# print(t.timeit(1))


class Analyze:
    def __init__(self):
        self.classifier_class = None
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

    # region Prepare data
    def save_stains(self, list_of_stains, mode, classified_type, name, numerator):
        """
        
        Parameters
        ----------
        list_of_stains : list
        mode : string
        classified_type : string
        name : string
        numerator : int

        Returns
        -------
        int
            updated numerator value
        """
        for ret_tuple in list_of_stains:
            adfIO.save(ret_tuple[0], './data/parsed/' + mode + '/' + classified_type + '/'
                       + name + '_' + numerator.__str__())
            numerator += 1
        return numerator
    
    def parse_slices(self, slices_tuple, yes_counters, no_counters, sep, axis):
        """
        Method responsible for turning sets of slices into training .adf files.

        Parameters
        ----------
        slices_tuple : tuple of lists
        yes_counters : tuple of ints
        no_counters : tuple of ints
        sep : Separator class instance
        axis : int

        Returns
        -------
        tuple, tuple
            Updated values of yes and no counters.
        """
        flair_yes = yes_counters[0]
        t1_yes = yes_counters[1]
        t1c_yes = yes_counters[2]
        t2_yes = yes_counters[3]
        flair_no = no_counters[0]
        t1_no = no_counters[1]
        t1c_no = no_counters[2]
        t2_no = no_counters[3]
        print("Dismantling FLAIR, axis "+axis.__str__())
        for imTuple in slices_tuple[0]:
            ret_list = sep.get_list_of_stains(imTuple)
            flair_yes = self.save_stains(ret_list, "flair", "tumor", "manual", flair_yes)
            nret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
            flair_no = self.save_stains(nret_list, "flair", "not", "flip", flair_no)
            auto_segmentation = seg.flair(imTuple[0])
            ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation,
                                                               imTuple[0])
            flair_yes = self.save_stains(ret_positive, "flair", "tumor", "auto", flair_yes)
            flair_no = self.save_stains(ret_negative, "flair", "not", "auto", flair_no)
        print("Dismantling T1, axis "+axis.__str__())
        for imTuple in slices_tuple[1]:
            ret_list = sep.get_list_of_stains(imTuple)
            t1_yes = self.save_stains(ret_list, "t1", "tumor", "manual", t1_yes)
            ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
            t1_no = self.save_stains(ret_list, "t1", "not", "flip", t1_no)
            auto_segmentation = seg.t1(imTuple[0])
            ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation,
                                                               imTuple[0])
            t1_yes = self.save_stains(ret_positive, "t1", "tumor", "auto", t1_yes)
            t1_no = self.save_stains(ret_negative, "t1", "not", "auto", t1_no)
        print("Dismantling T1C, axis "+axis.__str__())
        for imTuple in slices_tuple[2]:
            ret_list = sep.get_list_of_stains(imTuple)
            t1c_yes = self.save_stains(ret_list, "t1c", "tumor", "manual", t1c_yes)
            ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
            t1c_no = self.save_stains(ret_list, "t1c", "not", "flip", t1c_no)
            auto_segmentation = seg.t1c(imTuple[0])
            ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation,
                                                               imTuple[0])
            t1c_yes = self.save_stains(ret_positive, "t1c", "tumor", "auto", t1c_yes)
            t1c_no = self.save_stains(ret_negative, "t1c", "not", "auto", t1c_no)
        print("Dismantling T2, axis "+axis.__str__())
        for imTuple in slices_tuple[3]:
            ret_list = sep.get_list_of_stains(imTuple)
            t2_yes = self.save_stains(ret_list, "t2", "tumor", "manual", t2_yes)
            ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
            t2_no = self.save_stains(ret_list, "t2", "not", "flip", t2_no)
            auto_segmentation = seg.t2(imTuple[0])
            ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation,
                                                               imTuple[0])
            t2_yes = self.save_stains(ret_positive, "t2", "tumor", "auto", t2_yes)
            t2_no = self.save_stains(ret_negative, "t2", "not", "auto", t2_no)
        print("done")
        return (flair_yes, t1_yes, t1c_yes, t2_yes), (flair_no, t1_no, t1c_no, t2_no)
    # endregion

    # region Testing sub methods
    @staticmethod
    def create_patient_dir(patient):
        try:
            pathlib.Path("./classify/structured/"+patient).mkdir(parents=True)
        except OSError as exc:
            if exc.errno == 17:  # TODO check it
                shutil.rmtree("./classify/structured/"+patient, ignore_errors=True)
                pathlib.Path("./classify/structured/" + patient).mkdir(parents=True)
            else:
                raise

    def get_patient_id_from_dir(self, path, patient_dict):
        try:
            id = patient_dict[pathtools.get_folder_name_from_path(path, -2)]
        except TypeError:
            id = 0
        return id

    def get_parent_dir_name(self, path):
        return pathtools.get_folder_name_from_path(path, -1)

    def check_classify_input_dir(self):
        shutil.rmtree("./classify/structured/", ignore_errors=True)
        pathlib.Path("./classify/structured/").mkdir(parents=True)
        patient_dict = {}
        patient_id = 0
        for root, subFolders, files in os.walk('./classify/raw'):
            for folder in subFolders:
                if "brats" in folder:
                    patient_id += 1
                    self.create_patient_dir("pat_"+patient_id.__str__())
                    patient_dict[folder] = patient_id
            for file in files:
                if ".txt" in file:
                    os.remove(os.path.join(root, file))
                elif ".mha" in file:
                    shutil.copy2(os.path.join(root, file), "./classify/structured/" +
                                 self.get_patient_id_from_dir(root, patient_dict).__str__() + "/" + file)
        pass

    def generate_list_of_patients(self):
        """

        Returns
        -------
        list of tuples : (string, string, string, string, string)
            patient directory and file names.
        """
        patients_list = []
        flair_list = {}
        t1_list = {}
        t1c_list = {}
        t2_list = {}
        for rootd, subFolders, files in os.walk("./classify/structured"):
            for file in files:
                if "Flair" in file:
                    flair_list[self.get_parent_dir_name(rootd)] = file
                elif "T1." in file:
                    t1_list[self.get_parent_dir_name(rootd)] = file
                elif "T1c" in file:
                    t1c_list[self.get_parent_dir_name(rootd)] = file
                elif "T2" in file:
                    t2_list[self.get_parent_dir_name(rootd)] = file
        for i in range(flair_list.__len__()):  # TODO check it
            patients_list.append((i, flair_list[i], t1_list[i], t1c_list[i], t2_list[i]))
        return patients_list

    def generate_tumor_map(self, indexed_slices_list):
        # NOTES 1) use auto segmentation on slices
        # NOTES 2) use classification on slices
        # NOTES 3) multiply tumor slices by result of classification
        # NOTES 4) reconstruct mha brick from 3 axes of image type
        # TODO 5) merge all 4 type of classification
        # TODO 6) normalize mha brick
        # TODO 7) return result
        flair0 = []
        flair1 = []
        flair2 = []
        t10 = []
        t11 = []
        t12 = []
        t1c0 = []
        t1c1 = []
        t1c2 = []
        t20 = []
        t21 = []
        t22 = []
        sep = separator.Separator(3)
        # I had to: You are not supposed to understand this.
        for image in indexed_slices_list:
            for axis in image[0]:
                # region Mask slices classification
                for mslice in axis[0]:
                    accepted = []
                    stains_mask = (seg.flair(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_flair(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    flair0.append(stains_mask)
                for mslice in axis[1]:
                    accepted = []
                    stains_mask = (seg.flair(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_flair(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    flair1.append(stains_mask)
                for mslice in axis[2]:
                    accepted = []
                    stains_mask = (seg.flair(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_flair(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    flair2.append(stains_mask)
                # endregion
                # region Mask cuboid reconstruction
                flair0_array = recreate.create_3d_array(flair0, 0)
                flair1_array = recreate.create_3d_array(flair1, 1)
                flair2_array = recreate.create_3d_array(flair2, 2)
                flair_array = np.add(flair0_array, flair1_array)
                flair_array = np.add(flair_array, flair2_array)
                # endregion
            for axis in image[1]:
                # region Mask slices classification
                for mslice in axis[0]:
                    accepted = []
                    stains_mask = (seg.t1(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t1(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t10.append(stains_mask)
                for mslice in axis[1]:
                    accepted = []
                    stains_mask = (seg.t1(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t1(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t11.append(stains_mask)
                for mslice in axis[2]:
                    accepted = []
                    stains_mask = (seg.t1(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t1(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t12.append(stains_mask)
                # endregion
                # region Mask cuboid reconstruction
                t10_array = recreate.create_3d_array(t10, 0)
                t11_array = recreate.create_3d_array(t11, 1)
                t12_array = recreate.create_3d_array(t12, 2)
                t1_array = np.add(t10_array, t11_array)
                t1_array = np.add(t1_array, t12_array)
                # endregion
            for axis in image[2]:
                # region Mask slices classification
                for mslice in axis[0]:
                    accepted = []
                    stains_mask = (seg.t1c(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t1c(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t1c0.append(stains_mask)
                for mslice in axis[1]:
                    accepted = []
                    stains_mask = (seg.t1c(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t1c(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t1c1.append(stains_mask)
                for mslice in axis[2]:
                    accepted = []
                    stains_mask = (seg.t1c(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t1c(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t1c2.append(stains_mask)
                # endregion
                # region Mask cuboid reconstruction
                t1c0_array = recreate.create_3d_array(t1c0, 0)
                t1c1_array = recreate.create_3d_array(t1c1, 1)
                t1c2_array = recreate.create_3d_array(t1c2, 2)
                t1c_array = np.add(t1c0_array, t1c1_array)
                t1c_array = np.add(t1c_array, t1c2_array)
                # endregion
            for axis in image[3]:
                # region Mask slices classification
                for mslice in axis[0]:
                    accepted = []
                    stains_mask = (seg.t2(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t2(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t20.append(stains_mask)
                for mslice in axis[1]:
                    accepted = []
                    stains_mask = (seg.t2(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t2(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t21.append(stains_mask)
                for mslice in axis[2]:
                    accepted = []
                    stains_mask = (seg.t2(mslice[0])).astype(np.float)
                    if stains_mask.sum() != 0:
                        stains = sep.get_list_of_stains((mslice[0], stains_mask))
                        for stain in stains:
                            tumor, not_tumor = self.classifier_class.analyze_t2(stain[0])
                            # TODO check format of tumor not tumor (should obtain value from <0.0, 1.0>)
                            if tumor > not_tumor:
                                part = stain[1].astype(np.float)
                                part *= tumor
                                accepted.append((part, (stain[2], stain[3])))
                        new_mask = np.zeros(stains_mask.shape)
                        for elem in accepted:
                            new_mask_part = resizer.expand(elem[0], elem[1], elem[0].shape, new_mask.shape)
                            new_mask = np.add(new_mask, new_mask_part)
                        stains_mask = new_mask
                    t22.append(stains_mask)
                # endregion
                # region Mask cuboid reconstruction
                t20_array = recreate.create_3d_array(t20, 0)
                t21_array = recreate.create_3d_array(t21, 1)
                t22_array = recreate.create_3d_array(t22, 2)
                t2_array = np.add(t20_array, t21_array)
                t2_array = np.add(t2_array, t22_array)
                # endregion
        # region Mask cuboids compression

        # endregion
        # region Final cuboid normalization

        # endregion
        return 0
    # endregion

    # region Menu options
    def prepare_data(self):
        """
        Method responsible for converting input data from mha files to learning sets.
        """
        answer = input("Do you want to prepare training images (y/N): ")
        if 'Y' in answer.capitalize():
            subapp = Sorter()
            subapp.main()
        answer = input("Do you want to prepare training image pairs (y/N): ")
        sep = separator.Separator(10)
        if 'Y' in answer.capitalize():
            flair_yes = 0
            t1_yes = 0
            t1c_yes = 0
            t2_yes = 0
            flair_no = 0
            t1_no = 0
            t1c_no = 0
            t2_no = 0
            yes_counters = (flair_yes, t1_yes, t1c_yes, t2_yes)
            no_counters = (flair_no, t1_no, t1c_no, t2_no)
            self.check_parsed_dirs()
            for root, subFolders, files in os.walk("./data/raw/flair"):
                for file in files:
                    file_name_parts = file.split(".")
                    if file_name_parts[0] == 'pat1':  # TODO delete this line when testing finishes
                        print("Slicing file " + file_name_parts[0])
                        # Axis 0
                        flair, t1, t1c, t2 = mhaslicer.prepare_training_pairs(file_name_parts[0], axis=0)
                        slices_tuple = (flair, t1, t1c, t2)
                        yes_counters, no_counters = self.parse_slices(slices_tuple, yes_counters, no_counters, sep, 0)
                        # # Axis 1
                        # flair, t1, t1c, t2 = mhaslicer.prepare_training_pairs(file_name_parts[0], axis=1)
                        # slices_tuple = (flair, t1, t1c, t2)
                        # yes_counters, no_counters = self.parse_slices(slices_tuple, yes_counters, no_counters, sep, 1)
                        # # Axis 2
                        # flair, t1, t1c, t2 = mhaslicer.prepare_training_pairs(file_name_parts[0], axis=2)
                        # slices_tuple = (flair, t1, t1c, t2)
                        # yes_counters, no_counters = self.parse_slices(slices_tuple, yes_counters, no_counters, sep, 2)

    def teach_classifier(self):
        """
        Method responsible for teaching classifier basing on learning sets.
        """
        name = int(input('Please provide model name:'))
        test = input('Do you want to use advanced configuration? (y/N) ')
        if test.capitalize() == 'Y':
            # TODO implement asking for custom parameters
            teacher = teach.Teacher()
            teacher.teach(name)
        else:
            teacher = teach.Teacher()
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
                self.check_classify_input_dir()
            patients_list = self.generate_list_of_patients()
            for patient in patients_list:
                flair_slices = mhaslicer.prepare_testing_pairs(patient[1], patient[0])
                t1_slices = mhaslicer.prepare_testing_pairs(patient[2], patient[0])
                t1c_slices = mhaslicer.prepare_testing_pairs(patient[3], patient[0])
                t2_slices = mhaslicer.prepare_testing_pairs(patient[4], patient[0])
                # TESTME OutOfMemory risk !!!
                segmentation = self.generate_tumor_map((flair_slices, t1_slices, t1c_slices, t2_slices))
                mhaslicer.save_segmentation(segmentation, patient[0])
    # endregion

    # region Static functions
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
    # endregion


if __name__ == "__main__":
    app = Analyze()
    app.run()
