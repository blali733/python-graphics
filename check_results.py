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


for i in range(21):
    print("pat_", i)
    path = "./classify/structured/pat_" + i.__str__()
    ref_im = med_image_binearize(load_mha(path + "/more.mha"))
    ref = get_all_slices(ref_im)
    c30 = get_all_slices(load_mha(path + "/classification_3.0.mha"))
    c35 = get_all_slices(load_mha(path + "/classification_3.5.mha"))
    c40 = get_all_slices(load_mha(path + "/classification_4.0.mha"))
    c45 = get_all_slices(load_mha(path + "/classification_4.5.mha"))
    c50 = get_all_slices(load_mha(path + "/classification_5.0.mha"))
    c55 = get_all_slices(load_mha(path + "/classification_5.5.mha"))
    c60 = get_all_slices(load_mha(path + "/classification_6.0.mha"))
    c65 = get_all_slices(load_mha(path + "/classification_6.5.mha"))
    c70 = get_all_slices(load_mha(path + "/classification_7.0.mha"))
    c75 = get_all_slices(load_mha(path + "/classification_7.5.mha"))
    c80 = get_all_slices(load_mha(path + "/classification_8.0.mha"))
    c85 = get_all_slices(load_mha(path + "/classification_8.5.mha"))
    c90 = get_all_slices(load_mha(path + "/classification_9.0.mha"))
    c95 = get_all_slices(load_mha(path + "/classification_9.5.mha"))
    c100 = get_all_slices(load_mha(path + "/classification_10.0.mha"))
    c105 = get_all_slices(load_mha(path + "/classification_10.5.mha"))
    c110 = get_all_slices(load_mha(path + "/classification_11.0.mha"))
    c = (c30, c35, c40, c45, c50, c55, c60, c65, c70, c75, c80, c85, c90, c95, c100, c105, c110)
    ref_sum = ref_im.sum()
    overshoot = []
    common = []
    print("Files loaded!")
    for j in range(17):
        ovsh = 0
        com = 0
        ush = 0
        for k in range(len(ref)):
            tovsh, tcom, tush = raw_compare(c[j][k], ref[k])
            ovsh += tovsh
            com += tcom
            ush += tush
        overshoot.append(ovsh/ref_sum*100)
        common.append(com/ref_sum*100)
        print("Image " + j.__str__() + " calculated!")
    print("Values calculated!")
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(3.0, 11.5, 0.5), overshoot, label="False positive")
    plt.plot(np.arange(3.0, 11.5, 0.5), common, label="coverage")
    plt.title("False positives and coverage of analysis\nfor patient data.")
    plt.xlabel("Result binearization value")
    plt.ylabel("Percentage")
    plt.legend(loc="upper right")
    plt.savefig(path + "/results.png")
    print("Image saved!")
it = 0
for root, subFolders, files in os.walk('./classify'):
    for file in files:
        if '.png' in file:
            shutil.copy2(os.path.join(root, file), "./classify/image/" + it.__str__() + ".png")
            it += 1