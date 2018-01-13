# Windows only version, sorry
import sys
from imutils import medimageservicing as mcs
import matplotlib.pyplot as plt
import msvcrt


class Preview:
    plt.ion()
    def main(self):
        main_loop_fuse = 1
        while main_loop_fuse == 1:
            image_path = input("Image file in RAW directory: ")
            image_full_path = "./data/RAW/"+image_path
            image_data, image_header = mcs.med_load(image_full_path)
            axis = 0
            slice_id = 0
            fig = mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
            inner_loop_fuse = 1
            while inner_loop_fuse == 1:
                key = msvcrt.getwch()
                # print(key)
                if key == "Q":
                    inner_loop_fuse = 0
                if key == "X":
                    main_loop_fuse = 0
                    inner_loop_fuse = 0
                if key == "4":
                    if slice_id > 1:
                        slice_id -= 1
                        mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                if key == "6":
                    if slice_id < mcs.med_get_size(image_data, axis) - 1:
                        slice_id += 1
                        mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                if key == "7":
                    if slice_id > 5:
                        slice_id -= 5
                        mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                    else:
                        slice_id = 0
                        mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                if key == "9":
                    if slice_id < mcs.med_get_size(image_data, axis) - 5:
                        slice_id += 5
                        mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                    else:
                        slice_id = mcs.med_get_size(image_data, axis)
                        mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                if key == "8":
                    slice_id = 0
                    if axis < 2:
                        axis += 1
                    mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))
                if key == "2":
                    slice_id = 0
                    if axis > 0:
                        axis -= 1
                    mcs.med_plot(mcs.med_slice(image_data, axis, slice_id))


if __name__ == "__main__":
    app = Preview()
    app.main()
