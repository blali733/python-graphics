import SimpleITK as sitk


def get_all_slices(image, axis=0):
    slices = []
    if axis == 0:
        for i in range(image.shape[0]):
            slices.append(image[i, :, :])
    elif axis == 1:
        for i in range(image.shape[1]):
            slices.append(image[:, i, :])
    elif axis == 2:
        for i in range(image.shape[2]):
            slices.append(image[:, :, i])
    return slices


def get_nth_slice(med_image, axis, slice_id):
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


def load_mha(path):
    return sitk.GetArrayFromImage(sitk.ReadImage(path))


def save_mha(array_of_layers, path):
    sitk.WriteImage(sitk.GetImageFromArray(array_of_layers), path)
