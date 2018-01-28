# Preparation of data:
`version 1.0`  
* 3 axes: X, Y, Z
* Image sliced into parts according to consecutive axes
* Return pairs of image slice and corresponding mask
* Parsing of tuples into `*.adf` files:
1. Common parts of ground truth and image goes into `tumor` category
1. Mirrored copies of ground truth mask and corresponding image parts goes into `not tumor` category
1. Slice of image is parsed by automated segmentation procedure (1)
1. Basing on automated segmentation we separate mask into stains and divide them according to rules:
    1. stains which are correlated to ground truth in at least 80% are taken as `tumor` images
    1. stains with correlation ratio between 0 and 80% are discarded
    1. uncorrelated parts are saved as `not tumor` examples  

Process is executed for all images in input directory. 

Output files should be balanced between `tumor` and `not tumor` directories manually.


\-\-\-\-\-\-\-\-\-\-\-  
* (1) Segmentation algorithm
    * Image represented as numpy array with data type of `int16`, but with only positive values used
    are converted to `float` using conversion procedure of element-wise multiplication by:
    ```text
        1
    ----------
    max(int16)
    ```
    * Empirically defined ranges of pixel values, different for each image type are used to binearize image.