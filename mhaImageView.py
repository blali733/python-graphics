# Windows only version, sorry
from mhaDisplay import medImageServicing as msc
import matplotlib.pyplot as plt
from pimutils.mha import mhaMath
import numpy as np
try:
    from osutils import windows as osutil
except ImportError:
    from osutils import posix as osutil

# TODO clean this mess up


class Preview:
    def main(self):
        plt.ion()
        main_loop_fuse = 1
        while main_loop_fuse == 1:
            image_path = input("Image file in RAW directory: ")
            image_full_path = "./data/raw/"+image_path
            image_data = msc.med_load(image_full_path)
            axis = 0
            slice_id = 0
            fig = msc.med_plot(msc.med_slice(image_data, axis, slice_id))
            self.my_help()
            params = osutil.start_key_listener()
            inner_loop_fuse = 1
            single_mode_fuse = 1
            dual_mode_fuse = 0
            while inner_loop_fuse == 1:
                while single_mode_fuse == 1:
                    key = osutil.get_key_value()
                    # print(key)
                    if key == "Q":
                        inner_loop_fuse = 0
                        single_mode_fuse = 0
                        osutil.stop_key_listener(params)
                    elif key == "X":
                        main_loop_fuse = 0
                        inner_loop_fuse = 0
                        single_mode_fuse = 0
                        osutil.stop_key_listener(params)
                    elif key == "4":
                        if slice_id > 1:
                            slice_id -= 1
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    elif key == "6":
                        if slice_id < msc.med_get_size(image_data, axis) - 2:
                            slice_id += 1
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    elif key == "7":
                        if slice_id > 5:
                            slice_id -= 5
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                        else:
                            slice_id = 0
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    elif key == "9":
                        if slice_id < msc.med_get_size(image_data, axis) - 6:
                            slice_id += 5
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                        else:
                            slice_id = msc.med_get_size(image_data, axis)-1
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    elif key == "8":
                        slice_id = 0
                        if axis < 2:
                            axis += 1
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    elif key == "2":
                        slice_id = 0
                        if axis > 0:
                            axis -= 1
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    elif key == "5":
                        print(image_data.shape, image_data.dtype)
                        print(image_data.max(), image_data.min())
                    elif key == "3":
                        print("Saving file in csv format...")
                        msc.med_2_csv(msc.med_slice(image_data, axis, slice_id), image_path+"_"+axis.__str__()+"_"+slice_id.__str__())
                        print("File saved.")
                    elif key == "1":
                        # Switch to dual mode:
                        single_mode_fuse = 0
                        dual_mode_fuse = 1
                    elif key == "0":
                        t_slice = mhaMath.med_2_float(msc.med_slice(image_data, axis, slice_id))
                        msc.med_color_plot(np.stack((t_slice, t_slice, t_slice), axis=2))
                while dual_mode_fuse == 1:
                    osutil.stop_key_listener(params)
                    image2_path = input("Second image file in RAW directory: ")
                    image2_full_path = "./data/raw/" + image2_path
                    image2_data = msc.med_load(image2_full_path)
                    mask_cutoff = 0
                    osutil.start_key_listener()
                    msc.med_color_plot(
                        msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                    while dual_mode_fuse == 1:
                        key = osutil.get_key_value()
                        if key == "Q":
                            dual_mode_fuse = 0
                            single_mode_fuse = 1
                            # osutil.stop_key_listener(params)
                        elif key == "X":
                            dual_mode_fuse = 0
                            main_loop_fuse = 0
                            inner_loop_fuse = 0
                            osutil.stop_key_listener(params)
                        elif key == "4":
                            if slice_id > 1:
                                slice_id -= 1
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "6":
                            if slice_id < msc.med_get_size(image_data, axis) - 2:
                                slice_id += 1
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "7":
                            if slice_id > 5:
                                slice_id -= 5
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                            else:
                                slice_id = 0
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "9":
                            if slice_id < msc.med_get_size(image_data, axis) - 6:
                                slice_id += 5
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                            else:
                                slice_id = msc.med_get_size(image_data, axis) - 1
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "8":
                            slice_id = 0
                            if axis < 2:
                                axis += 1
                            msc.med_color_plot(
                                msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "2":
                            slice_id = 0
                            if axis > 0:
                                axis -= 1
                            msc.med_color_plot(
                                msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "1":
                            msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                        elif key == "0":
                            msc.med_color_plot(
                                msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "-":
                            if mask_cutoff > 0:
                                mask_cutoff -= 1
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        elif key == "+":
                            if mask_cutoff < image2_data.max():
                                mask_cutoff += 1
                                msc.med_color_plot(
                                    msc.med_dual_slice(image_data, image2_data, mask_cutoff, axis, slice_id))
                        
    def my_help(self):
        print("4, 7 - navigate left")
        print("6, 9 - navigate right")
        print("2, 8 - change axis")
        print("5 - File info")
        print("3 - save current slice to csv file")
        print("0 - show real colors")
        print("1 - enable mask overlay:")
        print("    1 - hide overlay")
        print("    0 - show overlay")
        print("    +/- - tweak overlay mask cutoff")
        print("Q - close image")
        print("X - exit")


if __name__ == "__main__":
    app = Preview()
    app.main()
