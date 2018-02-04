import numpy as np
from tools.mask import mirrorMask, separator
from tools.matrix import resizer, recreate
from tools.preparation.stains import save_stains
from tools.segmentation import segment


def parse_slices(slices_tuple, yes_counters, no_counters, sep, axis):
    """
    Method responsible for turning sets of slices into training .adf files.

    Parameters
    ----------
    slices_tuple : tuple of lists
        Tuple of lists of slices.
    yes_counters : tuple of ints
        Counters of tumor files per type.
    no_counters : tuple of ints
        Counters of not tumor files per type.
    sep : class
        Instance of separator class.
    axis : int
        Id of current axis.

    Returns
    -------
    tuple, tuple
        Updated values of yes and no counters.
    """
    # TODO Investigate bugs in mask mirroring
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
        flair_yes = save_stains(ret_list, "flair", "tumor", "manual", flair_yes)
        # nret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        # flair_no = save_stains(nret_list, "flair", "not", "flip", flair_no)
        auto_segmentation = segment.flair(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        flair_yes = save_stains(ret_positive, "flair", "tumor", "auto", flair_yes)
        flair_no = save_stains(ret_negative, "flair", "not", "auto", flair_no)
    print("Dismantling T1, axis "+axis.__str__())
    for imTuple in slices_tuple[1]:
        ret_list = sep.get_list_of_stains(imTuple)
        t1_yes = save_stains(ret_list, "t1", "tumor", "manual", t1_yes)
        # ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        # t1_no = save_stains(ret_list, "t1", "not", "flip", t1_no)
        auto_segmentation = segment.t1(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        t1_yes = save_stains(ret_positive, "t1", "tumor", "auto", t1_yes)
        t1_no = save_stains(ret_negative, "t1", "not", "auto", t1_no)
    print("Dismantling T1C, axis "+axis.__str__())
    for imTuple in slices_tuple[2]:
        ret_list = sep.get_list_of_stains(imTuple)
        t1c_yes = save_stains(ret_list, "t1c", "tumor", "manual", t1c_yes)
        # ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        # t1c_no = save_stains(ret_list, "t1c", "not", "flip", t1c_no)
        auto_segmentation = segment.t1c(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        t1c_yes = save_stains(ret_positive, "t1c", "tumor", "auto", t1c_yes)
        t1c_no = save_stains(ret_negative, "t1c", "not", "auto", t1c_no)
    print("Dismantling T2, axis "+axis.__str__())
    for imTuple in slices_tuple[3]:
        ret_list = sep.get_list_of_stains(imTuple)
        t2_yes = save_stains(ret_list, "t2", "tumor", "manual", t2_yes)
        # ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        # t2_no = save_stains(ret_list, "t2", "not", "flip", t2_no)
        auto_segmentation = segment.t2(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        t2_yes = save_stains(ret_positive, "t2", "tumor", "auto", t2_yes)
        t2_no = save_stains(ret_negative, "t2", "not", "auto", t2_no)
    print("done")
    return (flair_yes, t1_yes, t1c_yes, t2_yes), (flair_no, t1_no, t1c_no, t2_no)


def generate_tumor_map(classifier_class, indexed_slices_list):
    """
    Method responsible for classification train.

    Parameters
    ----------
    classifier_class : class
        Instance of classifier class
    indexed_slices_list : tuple
        Container of dismantled data for all images.

    Returns
    -------
    np.array
        Final cuboid with results of analysis.
    """
    # NOTES 1) use auto segmentation on slices
    # NOTES 2) use classification on slices
    # NOTES 3) multiply tumor slices by result of classification
    # NOTES 4) reconstruct mha brick from 3 axes of image type
    # NOTES 5) merge all 4 type of classification
    # NOTES 6) normalize mha brick
    # NOTES 7) return result
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
    # Flairs
    # region Mask slices classification
    for mslice in indexed_slices_list[0][0]:
        accepted = []
        stains_mask = (segment.flair(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_flair(stain[0])
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
    for mslice in indexed_slices_list[0][1]:
        accepted = []
        stains_mask = (segment.flair(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_flair(stain[0])
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
    for mslice in indexed_slices_list[0][2]:
        accepted = []
        stains_mask = (segment.flair(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_flair(stain[0])
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
    # T1s
    # region Mask slices classification
    for mslice in indexed_slices_list[1][0]:
        accepted = []
        stains_mask = (segment.t1(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t1(stain[0])
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
    for mslice in indexed_slices_list[1][1]:
        accepted = []
        stains_mask = (segment.t1(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t1(stain[0])
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
    for mslice in indexed_slices_list[1][2]:
        accepted = []
        stains_mask = (segment.t1(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t1(stain[0])
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
    # T1cs
    # region Mask slices classification
    for mslice in indexed_slices_list[2][0]:
        accepted = []
        stains_mask = (segment.t1c(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t1c(stain[0])
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
    for mslice in indexed_slices_list[2][1]:
        accepted = []
        stains_mask = (segment.t1c(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t1c(stain[0])
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
    for mslice in indexed_slices_list[2][2]:
        accepted = []
        stains_mask = (segment.t1c(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t1c(stain[0])
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
    # T2s:
    # region Mask slices classification
    for mslice in indexed_slices_list[3][0]:
        accepted = []
        stains_mask = (segment.t2(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t2(stain[0])
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
    for mslice in indexed_slices_list[3][1]:
        accepted = []
        stains_mask = (segment.t2(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t2(stain[0])
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
    for mslice in indexed_slices_list[3][2]:
        accepted = []
        stains_mask = (segment.t2(mslice[0])).astype(np.float)
        if stains_mask.sum() != 0:
            stains = sep.get_list_of_stains((mslice[0], stains_mask))
            for stain in stains:
                tumor, not_tumor = classifier_class.analyze_t2(stain[0])
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
    # Variables below had to be initialized in loops above, if they wouldn't - sth went wrong.
    # noinspection PyUnboundLocalVariable
    final_mask_cube = np.add(np.add(np.add(flair_array, t1_array), t1c_array), t2_array)
    # endregion
    # region Final cuboid normalization
    # TODO tweak parameter
    # final_mask_cube = recreate.binearize_3d_array(final_mask_cube, 3.0)
    # endregion
    return final_mask_cube
