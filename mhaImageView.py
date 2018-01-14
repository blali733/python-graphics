# Windows only version, sorry
import sys
from imutils import medimageservicing as msc
import matplotlib.pyplot as plt
try:
    from osutils import windows as osutil
except ImportError:
    from osutils import posix as osutil


class Preview:
    def main(self):
        osutil.start_key_listener()
        plt.ion()
        main_loop_fuse = 1
        while main_loop_fuse == 1:
            image_path = input("Image file in RAW directory: ")
            image_full_path = "./data/RAW/"+image_path
            image_data, image_header = msc.med_load(image_full_path)
            axis = 0
            slice_id = 0
            fig = msc.med_plot(msc.med_slice(image_data, axis, slice_id))
            self.my_help()
            inner_loop_fuse = 1
            while inner_loop_fuse == 1:
                key = osutil.get_key_value()
                # print(key)
                if key == "Q":
                    inner_loop_fuse = 0
                if key == "X":
                    main_loop_fuse = 0
                    inner_loop_fuse = 0
                    osutil.stop_key_listener()
                if key == "4":
                    if slice_id > 1:
                        slice_id -= 1
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                if key == "6":
                    if slice_id < msc.med_get_size(image_data, axis) - 1:
                        slice_id += 1
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                if key == "7":
                    if slice_id > 5:
                        slice_id -= 5
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    else:
                        slice_id = 0
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                if key == "9":
                    if slice_id < msc.med_get_size(image_data, axis) - 5:
                        slice_id += 5
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                    else:
                        slice_id = msc.med_get_size(image_data, axis)
                        msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                if key == "8":
                    slice_id = 0
                    if axis < 2:
                        axis += 1
                    msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                if key == "2":
                    slice_id = 0
                    if axis > 0:
                        axis -= 1
                    msc.med_plot(msc.med_slice(image_data, axis, slice_id))
                if key == "5":
                    print(image_data.shape, image_data.dtype)
                if key == "3":
                    print("Saving file in csv format...")
                    msc.med_2_csv(msc.med_slice(image_data, axis, slice_id), image_path+"_"+axis.__str__()+"_"+slice_id.__str__())
                    print("File saved.")

    def my_help(self):
        print("4, 7 - navigate left")
        print("6, 9 - navigate right")
        print("2, 8 - change axis")
        print("5 - File info")
        print("3 - save current slice to csv file")
        print("Q - close image")
        print("X - exit")


if __name__ == "__main__":
    app = Preview()
    app.main()
