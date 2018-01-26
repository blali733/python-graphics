from osutils.fileIO import adfIO


def save_stains(list_of_stains, mode, classified_type, name, enumerator):
    """

    Parameters
    ----------
    list_of_stains : list
    mode : string
    classified_type : string
    name : string
    enumerator : int

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