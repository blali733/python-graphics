import numpy as np


def create_3d_array(layers_list, axis):
    # TODO check if it couldn't be optimized by usage of numpy functions
    dtype = layers_list[0].dtype
    shape = layers_list[0].shape
    if axis == 0:
        array_3d = np.zeros((layers_list.__len__(), shape[0], shape[1]), dtype=dtype)
        layer_id = 0
        for layer in layers_list:
            array_3d[layer_id, :, :] = layer
            layer_id += 1
    elif axis == 1:
        array_3d = np.zeros((shape[0], layers_list.__len__(), shape[1]), dtype=dtype)
        layer_id = 0
        for layer in layers_list:
            array_3d[:, layer_id, :] = layer
            layer_id += 1
    else:
        array_3d = np.zeros((shape[0], shape[1], layers_list.__len__()), dtype=dtype)
        layer_id = 0
        for layer in layers_list:
            array_3d[:, :, layer_id] = layer
            layer_id += 1
    return array_3d


def binearize_3d_array(array, offset):
    return (array > offset)*1
