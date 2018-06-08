import matplotlib
# set the matplotlib backend so figures can be saved in the background
import shutil

matplotlib.use("Agg")
from src.osutils.fileIO.mhaIO import load_mha
from src.tools.mha.mhaSlicer import get_all_slices
from src.tools.mha.mhaMath import med_image_binearize
from src.tools.mask.comparator import raw_compare
import matplotlib.pyplot as plt
import numpy as np
import os


global_data_ovsh = {
    "ln10": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "ln25": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "ln50": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "svgg10": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "svgg25": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "svgg50": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
global_data_match = {
    "ln10": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "ln25": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "ln50": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "svgg10": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "svgg25": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "svgg50": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
for i in range(16):
    print("pat_", i)
    path = "./classify/structured/pat_" + i.__str__()
    ref_im = med_image_binearize(load_mha(path + "/more.mha"))
    ref = get_all_slices(ref_im)
    ln10_05 = get_all_slices(load_mha(path + "/LN10_05.mha"))
    ln10_07 = get_all_slices(load_mha(path + "/LN10_07.mha"))
    ln10_09 = get_all_slices(load_mha(path + "/LN10_09.mha"))
    ln10_11 = get_all_slices(load_mha(path + "/LN10_11.mha"))
    ln10_13 = get_all_slices(load_mha(path + "/LN10_13.mha"))
    ln10_15 = get_all_slices(load_mha(path + "/LN10_15.mha"))
    ln10_17 = get_all_slices(load_mha(path + "/LN10_17.mha"))
    ln10_19 = get_all_slices(load_mha(path + "/LN10_19.mha"))
    ln10_21 = get_all_slices(load_mha(path + "/LN10_21.mha"))
    ln10_23 = get_all_slices(load_mha(path + "/LN10_23.mha"))
    ln10_25 = get_all_slices(load_mha(path + "/LN10_25.mha"))
    ln10 = (ln10_05, ln10_07, ln10_09, ln10_11, ln10_13, ln10_15, ln10_17, ln10_19, ln10_21, ln10_23, ln10_25)
    ln25_05 = get_all_slices(load_mha(path + "/LN25_05.mha"))
    ln25_07 = get_all_slices(load_mha(path + "/LN25_07.mha"))
    ln25_09 = get_all_slices(load_mha(path + "/LN25_09.mha"))
    ln25_11 = get_all_slices(load_mha(path + "/LN25_11.mha"))
    ln25_13 = get_all_slices(load_mha(path + "/LN25_13.mha"))
    ln25_15 = get_all_slices(load_mha(path + "/LN25_15.mha"))
    ln25_17 = get_all_slices(load_mha(path + "/LN25_17.mha"))
    ln25_19 = get_all_slices(load_mha(path + "/LN25_19.mha"))
    ln25_21 = get_all_slices(load_mha(path + "/LN25_21.mha"))
    ln25_23 = get_all_slices(load_mha(path + "/LN25_23.mha"))
    ln25_25 = get_all_slices(load_mha(path + "/LN25_25.mha"))
    ln25 = (ln25_05, ln25_07, ln25_09, ln25_11, ln25_13, ln25_15, ln25_17, ln25_19, ln25_21, ln25_23, ln25_25)
    ln50_05 = get_all_slices(load_mha(path + "/LN50_05.mha"))
    ln50_07 = get_all_slices(load_mha(path + "/LN50_07.mha"))
    ln50_09 = get_all_slices(load_mha(path + "/LN50_09.mha"))
    ln50_11 = get_all_slices(load_mha(path + "/LN50_11.mha"))
    ln50_13 = get_all_slices(load_mha(path + "/LN50_13.mha"))
    ln50_15 = get_all_slices(load_mha(path + "/LN50_15.mha"))
    ln50_17 = get_all_slices(load_mha(path + "/LN50_17.mha"))
    ln50_19 = get_all_slices(load_mha(path + "/LN50_19.mha"))
    ln50_21 = get_all_slices(load_mha(path + "/LN50_21.mha"))
    ln50_23 = get_all_slices(load_mha(path + "/LN50_23.mha"))
    ln50_25 = get_all_slices(load_mha(path + "/LN50_25.mha"))
    ln50 = (ln50_05, ln50_07, ln50_09, ln50_11, ln50_13, ln50_15, ln50_17, ln50_19, ln50_21, ln50_23, ln50_25)
    svgg10_05 = get_all_slices(load_mha(path + "/SVGG10_05.mha"))
    svgg10_07 = get_all_slices(load_mha(path + "/SVGG10_07.mha"))
    svgg10_09 = get_all_slices(load_mha(path + "/SVGG10_09.mha"))
    svgg10_11 = get_all_slices(load_mha(path + "/SVGG10_11.mha"))
    svgg10_13 = get_all_slices(load_mha(path + "/SVGG10_13.mha"))
    svgg10_15 = get_all_slices(load_mha(path + "/SVGG10_15.mha"))
    svgg10_17 = get_all_slices(load_mha(path + "/SVGG10_17.mha"))
    svgg10_19 = get_all_slices(load_mha(path + "/SVGG10_19.mha"))
    svgg10_21 = get_all_slices(load_mha(path + "/SVGG10_21.mha"))
    svgg10_23 = get_all_slices(load_mha(path + "/SVGG10_23.mha"))
    svgg10_25 = get_all_slices(load_mha(path + "/SVGG10_25.mha"))
    svgg10 = (svgg10_05, svgg10_07, svgg10_09, svgg10_11, svgg10_13, svgg10_15, svgg10_17, svgg10_19, svgg10_21, svgg10_23, svgg10_25)
    svgg25_05 = get_all_slices(load_mha(path + "/SVGG25_05.mha"))
    svgg25_07 = get_all_slices(load_mha(path + "/SVGG25_07.mha"))
    svgg25_09 = get_all_slices(load_mha(path + "/SVGG25_09.mha"))
    svgg25_11 = get_all_slices(load_mha(path + "/SVGG25_11.mha"))
    svgg25_13 = get_all_slices(load_mha(path + "/SVGG25_13.mha"))
    svgg25_15 = get_all_slices(load_mha(path + "/SVGG25_15.mha"))
    svgg25_17 = get_all_slices(load_mha(path + "/SVGG25_17.mha"))
    svgg25_19 = get_all_slices(load_mha(path + "/SVGG25_19.mha"))
    svgg25_21 = get_all_slices(load_mha(path + "/SVGG25_21.mha"))
    svgg25_23 = get_all_slices(load_mha(path + "/SVGG25_23.mha"))
    svgg25_25 = get_all_slices(load_mha(path + "/SVGG25_25.mha"))
    svgg25 = (
    svgg25_05, svgg25_07, svgg25_09, svgg25_11, svgg25_13, svgg25_15, svgg25_17, svgg25_19, svgg25_21, svgg25_23,
    svgg25_25)
    svgg50_05 = get_all_slices(load_mha(path + "/SVGG50_05.mha"))
    svgg50_07 = get_all_slices(load_mha(path + "/SVGG50_07.mha"))
    svgg50_09 = get_all_slices(load_mha(path + "/SVGG50_09.mha"))
    svgg50_11 = get_all_slices(load_mha(path + "/SVGG50_11.mha"))
    svgg50_13 = get_all_slices(load_mha(path + "/SVGG50_13.mha"))
    svgg50_15 = get_all_slices(load_mha(path + "/SVGG50_15.mha"))
    svgg50_17 = get_all_slices(load_mha(path + "/SVGG50_17.mha"))
    svgg50_19 = get_all_slices(load_mha(path + "/SVGG50_19.mha"))
    svgg50_21 = get_all_slices(load_mha(path + "/SVGG50_21.mha"))
    svgg50_23 = get_all_slices(load_mha(path + "/SVGG50_23.mha"))
    svgg50_25 = get_all_slices(load_mha(path + "/SVGG50_25.mha"))
    svgg50 = (
    svgg50_05, svgg50_07, svgg50_09, svgg50_11, svgg50_13, svgg50_15, svgg50_17, svgg50_19, svgg50_21, svgg50_23,
    svgg50_25)
    ref_sum = ref_im.sum()
    results = (ln10, ln25, ln50, svgg10, svgg25, svgg50)
    result_names = ("ln10", "ln25", "ln50", "svgg10", "svgg25", "svgg50")
    print("Files loaded!")
    for c, n in zip(results, result_names):
        overshoot = []
        common = []
        for j in range(11):
            ovsh = 0
            com = 0
            ush = 0
            for k in range(len(ref)):
                tovsh, tcom, tush = raw_compare(c[j][k], ref[k])
                ovsh += tovsh
                com += tcom
                ush += tush
            overshoot.append(ovsh/ref_sum*100)
            global_data_ovsh[n][j] += ovsh/ref_sum*100
            common.append(com/ref_sum*100)
            global_data_match[n][j] += com/ref_sum*100
            print("Image " + j.__str__() + " calculated!")
        print("Values calculated!")
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(np.arange(0.5, 2.7, 0.2), overshoot, label="False positive")
        plt.plot(np.arange(0.5, 2.7, 0.2), common, label="coverage")
        plt.title("False positives and coverage of analysis\nfor patient data. ({})".format(n))
        plt.xlabel("Result binearization value")
        plt.ylabel("Percentage")
        plt.legend(loc="upper right")
        plt.savefig("{}/pat_{}_{}.png".format(path, i, n))
        print("Image saved!")
tab = ("ln10", "ln25", "ln50", "svgg10", "svgg25", "svgg50")
for res in tab:
    for i in range(11):
        global_data_match[res][i] /= 16
        global_data_ovsh[res][i] /= 16
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0.5, 2.7, 0.2), global_data_ovsh[res], label="False positive")
    plt.plot(np.arange(0.5, 2.7, 0.2), global_data_match[res], label="coverage")
    plt.title("False positives and coverage of analysis\nfor all test cases")
    plt.xlabel("Result binearization value")
    plt.ylabel("Percentage")
    plt.legend(loc="upper right")
    plt.savefig("./classify/structured/global_{}.png".format(res))
    print("Image saved!")
