# Viewer of *mha* image files:
`version 1.0`  
This part allows user to observe content of `mha` file as set of 2d images, sliced according to given axis.

Images could be represented in different coloring modes:
* local relative - white value is equal to local slice maximum
* global relative - white value is equal to maximum of whole file

Application is also capable of displaying such image in *"masked"* mode - after loading file with data, second file
representing segmentation (such as ground truth, or result of segmentation by our software) could be loaded as mask,
which would result in displaying common parts as grayscale, and rest of base image as shades of red. Such representation
allows to have visual correlation between results and data.