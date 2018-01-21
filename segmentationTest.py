from pimutils.mha import mhaIO
from pimutils.segmentation import segment
from pimutils.mask import comparator

flair = mhaIO.load_mha("./data/raw/flair.mha")
flair_slices = mhaIO.get_all_slices(flair)

def test():
    # region Image loading
    flair = mhaIO.load_mha("./data/raw/flair.mha")
    t1 = mhaIO.load_mha("./data/raw/t1.mha")
    t1c = mhaIO.load_mha("./data/raw/t1c.mha")
    t2 = mhaIO.load_mha("./data/raw/t2.mha")
    more = mhaIO.load_mha("./data/raw/more.mha")
    flair_slices = mhaIO.get_all_slices(flair)
    t1_slices = mhaIO.get_all_slices(t1)
    t1c_slices = mhaIO.get_all_slices(t1c)
    t2_slices = mhaIO.get_all_slices(t2)
    more_slices = mhaIO.get_all_slices(more)
    # endregion
    # TODO using flair_slices, t1_slices, t1c_slices, t2_slices check segmentation
    # region Statistics
    f_comm = 0
    f_oversh = 0
    t1_comm = 0
    t1_oversh = 0
    t1c_comm = 0
    t1c_oversh = 0
    t2_comm = 0
    t2_oversh = 0
    for i in range(flair_slices.__len__()):
        fcom, fovs = comparator.compare(more_slices[i], segment.flair(flair_slices[i]), True)
        t1com, t1ovs = comparator.compare(more_slices[i], segment.t1(t1_slices[i]), True)
        t1ccom, t1covs = comparator.compare(more_slices[i], segment.t1c(t1c_slices[i]), True)
        t2com, t2ovs = comparator.compare(more_slices[i], segment.t2(t2_slices[i]), True)
        f_comm += fcom
        f_oversh += fovs
        t1_comm += t1com
        t1_oversh += t1ovs
        t1c_comm += t1ccom
        t1c_oversh += t1covs
        t2_comm += t2com
        t2_oversh += t2ovs
    f_comm /= flair_slices.__len__()
    f_oversh /= flair_slices.__len__()
    t1_comm /= flair_slices.__len__()
    t1_oversh /= flair_slices.__len__()
    t1c_comm /= flair_slices.__len__()
    t1c_oversh /= flair_slices.__len__()
    t2_comm /= flair_slices.__len__()
    t2_oversh /= flair_slices.__len__()
    print("Averages:")
    print("flair: common "+f_comm.__str__()+"%; overshot: "+f_oversh.__str__())
    print("t1: common " + t1_comm.__str__() + "%; overshot: " + t1_oversh.__str__())
    print("t1c: common " + t1c_comm.__str__() + "%; overshot: " + t1c_oversh.__str__())
    print("t2: common " + t2_comm.__str__() + "%; overshot: " + t2_oversh.__str__())
    #endregion

if __name__ == "__main__":
    test()