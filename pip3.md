### This file contais list of required modules with reason should be kept:
#### Data preparation:
|Name|Reason|Notes
|---|---|---|
|numpy|Mathematical operations on arrays| |
|scipy*|Imresize function|Used in slice resizing to meet classifier requirements|
|matplotlib|Displaying of np.arrays as images| |
|simpleitk|Operations on MHA files.|https://stackoverflow.com/a/42594949|
|cv2|||
|pillow|Imresize function|Used in slice resizing to meet classifier requirements, replacement of `scipy.misc.imresize`|
#### machine learning:
|Name|Reason|Notes
|---|---|---|
|keras| | |
|sklearn| | |
|tensorflow| | |
|h5py|Allows model saving| |
>Packages which are installing themselves as dependencies are not listed here.