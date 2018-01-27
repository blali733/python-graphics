from mhaDisplay import medImageServicing as msc
import matplotlib.pyplot as plt
try:
    from mhaDisplay import windows as osutil
except ImportError:
    from mhaDisplay import posix as osutil

# TODO catch and service exception on wrong files.


class Preview:
    def __init__(self):
        self.imageService = msc.Plotter()
        self.mode = 0
        self.params = None
        self.inner_loop_fuse = 1
        self.main_loop_fuse = 1

    def main(self):
        plt.ion()
        while self.main_loop_fuse == 1:
            image_path = input("MHA image path: ")
            self.imageService.set_image(image_path)
            self.my_help()
            self.params = osutil.start_key_listener()
            self.inner_loop_fuse = 1
            while self.inner_loop_fuse == 1:
                key = osutil.get_key_value()
                self.service_key(key)

    def service_key(self, key):
        if key == "9":
            self.imageService.next_layer(5)
        elif key == "6":
            self.imageService.next_layer()
        elif key == "7":
            self.imageService.prev_layer(5)
        elif key == "4":
            self.imageService.prev_layer()
        elif key == "8":
            self.imageService.next_axis()
        elif key == "2":
            self.imageService.previous_axis()
        elif key == "5":
            self.imageService.get_info()
        elif key == "3":
            self.imageService.med_2_csv()
        elif key == "1":
            if self.mode == 1:
                self.imageService.toggle_overlay()
            else:
                try:
                    osutil.stop_key_listener(self.params)
                    path = input("Please give path to mask in MHA format: ")
                    self.imageService.set_mask(path)
                    self.params = osutil.start_key_listener()
                    self.mode = 1
                except TypeError as e:
                    print(e.args[0])
        elif key == "Q":
            if self.mode == 1:
                self.imageService.unset_mask()
                self.mode = 0
            else:
                self.inner_loop_fuse = 0
        elif key == "X":
            self.main_loop_fuse = 0
            self.inner_loop_fuse = 0
        elif key == "c":
            self.imageService.toggle_relativity()

                        
    def my_help(self):
        print("4, 7 - navigate left")
        print("6, 9 - navigate right")
        print("2, 8 - change axis")
        print("5 - File info")
        print("3 - save current slice to csv file")
        print("c - toggle relativity mode")
        print("1 - enable mask overlay:")
        print("    1 - hide overlay")
        print("    0 - show overlay")
        print("    +/- - tweak overlay mask cutoff")
        print("Q - close image")
        print("X - exit")


if __name__ == "__main__":
    app = Preview()
    app.main()
