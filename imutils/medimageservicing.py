# from medpy.io import load
import SimpleITK as sitk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pathlib


def med_load(path):
    i = sitk.GetArrayFromImage(sitk.ReadImage(path))
    return i, 0


def med_slice(med_image, axis, slice_id):
    if axis == 0:
        if slice_id <= med_image.shape[0]:
            return med_image[slice_id, :, :]
        else:
            return 0
    elif axis == 1:
        if slice_id <= med_image.shape[1]:
            return med_image[:, slice_id, :]
        else:
            return 0
    else:
        if slice_id <= med_image.shape[2]:
            return med_image[:, :, slice_id]
        else:
            return 0


def med_plot(med_image_slice):
    plt.imshow(med_image_slice, cmap=cm.Greys_r)
    # plt.show(block=False)
    plt.pause(0.0001)


def med_get_size(med_image, axis):
    if axis == 0:
        return med_image.shape[0]
    elif axis == 1:
        return med_image.shape[1]
    else:
        return med_image.shape[2]


def med_2_csv(med_image_slice, csv_file_name):
    pathlib.Path('./data/raw/csv').mkdir(parents=True, exist_ok=True)
    file = open("./data/raw/csv/"+csv_file_name+".csv", "w")
    for y in range(med_image_slice.shape[1]):
        for x in range(med_image_slice.shape[0]):
            file.write(med_image_slice[y, x].__str__()+"; ")
        file.write("\n")
    file.close()
