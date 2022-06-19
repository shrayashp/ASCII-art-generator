# ASCII-art-generator
----
The ASCII (American Standard Code for Information Interchange) is a well known character encoding standard, used for representing text data in computers and electronic communication. <br />
In this project, I have created an ASCII Art Generator, which converts images and videos to ASCII art, which has ASCII characters instead of pixels, i.e., the images and videos are pieced together from 70 ASCII characters.<br />
An example is shown below:<br />
<br/>
![hib](https://user-images.githubusercontent.com/76247110/174473416-53d71f80-bc09-4474-bed3-694e1ab9d1b2.png) <br/>
If we zoom in on the ASCII image, we see that the image is composed of tiny ASCII characters. <br/>
### How to run the project ###
----
#### Dependencies required to run
* Python3 must be installed and path must be set
* Following python packages must be installed and up to date:
    * cv2
    * PIL
    * argparse
    * os
    * shutil
    * numpy
#### Steps to run:
* Clone this repository
* In terminal, change the working directory to wherever you have cloned this repository
* If you wish to convert an image to its ASCII art, run the following command in the terminal
    * _python genasciiart.py --file fname --scale s --out outfname --numcols n_ \
Here in place of _fname_, put the name of the file which you wish to convert to ASCII art, inplace of _s_, put the required scale, which denotes the ratio between height of 1 cell and width of 1 cell, inplace of _outfname_ , put the name of the file in which you want the output, and inplace of _n_ put the number of columns of cells you want in the output image. Here, we have set default values of output file as out.jpg, of s as 2 and of num_cols as 200, but you are free to change these values as you desire, by the command line given above.
* If you wish to convert a video to its ASCII video, run the following command in the terminal
    * _python genasciivid.py --file fname --out outfname --fps f --numcols n_ \
Here in place of _fname_, put the name of the file which you wish to convert to ASCII video, inplace of _outfname_ , put the name of the file in which you want the output, inplace of _f_ put the required fps of the output video, i.e. how many frames per second you require in the output video, and inplace of _n_ put the number of columns of cells you want in the output image. Here we have set the scale to a default value of 2, as this value works well for most images. Also, we have set default values of output file as out.mp4, of fps as 10 and of num_cols as 400, but you are free to change these values as you desire, by the command line given above. 
