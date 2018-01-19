# Array Data File format
# created by M. Urbaniak 2018
# For reference consult ADF.md file
import numpy as np
# TODO: Ensure endian safety if used to move data between different systems!


def save(array, path):
    """
    Saves array to file.

    Parameters
    ----------
    array : nparray
        2 dimensional aray to be serialized
    path : string
        path of output file

    Returns
    -------
    int
        result code: 0 - OK, <0 - error
    """
    # version and data-type code:
    code = 1 << 4
    if array.dtype == np.int16:
        code += 0
        type = np.int16
    elif array.dtype == np.int32:
        code += 1
        type = np.int32
    else:
        print("Unsupported data type! "+array.dtype.__str__())
        return -1
    with open(path+'.adf', "wb") as f:
        f.write(bytes([0x41, 0x44, 0x46]))
        f.write(code.to_bytes(1, byteorder='big'))
        f.write(array.shape[0].to_bytes(2, byteorder='big'))
        f.write(array.shape[1].to_bytes(2, byteorder='big'))
        f.write(bytes([0xff]))
        f.write(array.tobytes())  # MIGHT break endian handling
    return 0


def load(path):
    """
    Deserializes file into np array.

    Parameters
    ----------
    path : string
        Path of file to be deserialized

    Returns
    -------
    int or nparray
        int as error code, or np array on success.
    """
    with open(path+'.adf', "rb") as f:
        head = f.read(3)
        if head == bytes([0x41, 0x44, 0x46]):
            val = f.read(1)
            val = int.from_bytes(val, byteorder='big', signed=False)
            data_type = val - (val >> 4 << 4)
            if data_type == 0:
                data_type = np.int16
            elif data_type == 1:
                data_type = np.int32
            else:
                return -1
            x = int.from_bytes(f.read(2), byteorder='big')
            y = int.from_bytes(f.read(2), byteorder='big')
            f.read(1)
            array = np.frombuffer(f.read(), dtype=data_type)
            array = np.reshape(array, [x, y])
            return array
        else:
            return -1
