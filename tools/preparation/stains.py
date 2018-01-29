from osutils.fileIO import adfIO


def save_stains(list_of_stains, mode, classified_type, name, enumerator):
    """
    Method responsible for saving all stains in list as ADF files.

    Parameters
    ----------
    list_of_stains : list
        List of separated stains.
    mode : string
        Name of source image type (flair, t1, t1c, t2).
    classified_type : string
        String representation of classification type (tumor, not).
    name : string
        Name of file.
    enumerator : int
        Id of file.

    Returns
    -------
    int
        updated numerator value
    """
    for ret_tuple in list_of_stains:
        adfIO.save(ret_tuple[0], './data/parsed/' + mode + '/' + classified_type + '/'
                   + name + '_' + enumerator.__str__())
        enumerator += 1
    return enumerator
