from os import name as os_name


def get_folder_name_from_path(path, dir_position):
    """
    Method responsible for slicing pathstring according to system path separators.

    Parameters
    ----------
    path : pathstring
        String representation of path to be sliced
    dir_position : int
        Id of element which would be extracted

    Returns
    -------
    string
        Part of path with desired index or empty string on error.
    """
    if os_name == "nt":
        folders = path.split('\\')
    else:
        folders = path.split('/')
    try:
        return folders[dir_position]
    except IndexError:
        raise IndexError("Index not in range!")
