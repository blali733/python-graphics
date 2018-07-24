<img src="https://img.shields.io/badge/status-Stalled-yellow.svg">&nbsp;&nbsp;[![Build Status](https://travis-ci.org/blali733/python-graphics.svg?branch=master)](https://travis-ci.org/blali733/python-graphics)

# Medical image classifier:
### System requirements:
Project is written in Python 3. Tested under Python 3.6 on Windows 10 x64 and Ubuntu 17.10 x64.  
List of required modules is accessible in pip3 file ([pip3.md](pip3.md))
### Documentation of application:
Documentation of used algorithms is located in `documentation` directory.  
Links to most important parts:
* [1. Preparation of learning sets](documentation/PrepareData.md)
* [2. Building and teaching classifier](documentation/ClassifierLearning.md)
* [3. Classification of images](documentation/ImageClassification.md)
* [*MHA* image viewer](documentation/mhaImageView.md)
### Solution editing:
This solution was prepared using PyCharm community edition. Recommended modification to settings of
environment to maintain common standards could be found in [settings](Settings.md) file.
### Remarks:
All algorithms which implementation is based on work performed by another authors have source denoted in first line 
comment. For ease we have also stated those sources below:

- LeNet classifier model implementation is based on 
[this post](https://www.pyimagesearch.com/2017/12/11/image-classification-with-keras-and-deep-learning/)
by Adrian Rosebrock. Training and testing procedures for classifiers were also inspired by mentioned source.

- SmallerVGGNet classifier model implementation is based on 
[this post](https://www.pyimagesearch.com/2018/04/16/keras-and-convolutional-neural-networks-cnns/)
by Adrian Rosebrock.

- VGGNet classifier model implementation is based on 
[this repository](http://dandxy89.github.io/ImageModels/vgg19/)
by dandxy89.
