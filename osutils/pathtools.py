import os


def get_folder_name_from_path(path, dir_position):
    if os.name == "nt":
        folders = path.split('\\')
    else:
        folders = path.split('/')
    return folders[dir_position]