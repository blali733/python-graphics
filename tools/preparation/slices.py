from tools.mask import mirrorMask
from tools.preparation.stains import save_stains
from tools.segmentation import segment


def parse_slices(slices_tuple, yes_counters, no_counters, sep, axis):
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
        flair_yes = save_stains(ret_list, "flair", "tumor", "manual", flair_yes)
        nret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        flair_no = save_stains(nret_list, "flair", "not", "flip", flair_no)
        auto_segmentation = seg.flair(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        flair_yes = save_stains(ret_positive, "flair", "tumor", "auto", flair_yes)
        flair_no = save_stains(ret_negative, "flair", "not", "auto", flair_no)
    print("Dismantling T1, axis "+axis.__str__())
    for imTuple in slices_tuple[1]:
        ret_list = sep.get_list_of_stains(imTuple)
        t1_yes = save_stains(ret_list, "t1", "tumor", "manual", t1_yes)
        ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        t1_no = save_stains(ret_list, "t1", "not", "flip", t1_no)
        auto_segmentation = seg.t1(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        t1_yes = save_stains(ret_positive, "t1", "tumor", "auto", t1_yes)
        t1_no = save_stains(ret_negative, "t1", "not", "auto", t1_no)
    print("Dismantling T1C, axis "+axis.__str__())
    for imTuple in slices_tuple[2]:
        ret_list = sep.get_list_of_stains(imTuple)
        t1c_yes = save_stains(ret_list, "t1c", "tumor", "manual", t1c_yes)
        ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        t1c_no = save_stains(ret_list, "t1c", "not", "flip", t1c_no)
        auto_segmentation = seg.t1c(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        t1c_yes = save_stains(ret_positive, "t1c", "tumor", "auto", t1c_yes)
        t1c_no = save_stains(ret_negative, "t1c", "not", "auto", t1c_no)
    print("Dismantling T2, axis "+axis.__str__())
    for imTuple in slices_tuple[3]:
        ret_list = sep.get_list_of_stains(imTuple)
        t2_yes = save_stains(ret_list, "t2", "tumor", "manual", t2_yes)
        ret_list = mirrorMask.flip_and_check(imTuple[0], imTuple[1], ret_list)
        t2_no = save_stains(ret_list, "t2", "not", "flip", t2_no)
        auto_segmentation = seg.t2(imTuple[0])
        ret_positive, ret_negative = sep.find_common_parts(imTuple[1], ret_list, auto_segmentation, imTuple[0])
        t2_yes = save_stains(ret_positive, "t2", "tumor", "auto", t2_yes)
        t2_no = save_stains(ret_negative, "t2", "not", "auto", t2_no)
    print("done")
    return (flair_yes, t1_yes, t1c_yes, t2_yes), (flair_no, t1_no, t1c_no, t2_no)