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
### Internal Working of the project
The working of this project is based on the representation of images in python. A RGB color image can be considered to be consist of 3 images, a red scale, a blue scale and a green scale. Each of these is an 2D array of pixel values ranging from 0 to 255. So, an image can be considered as a 2D array of tuples (x, y, z), with x, y, z ranging from 0 to 255. <br/>
To convert the given image into an ASCII art, we use a character map, where the characters are arranged in ascending order of luminosity, i.e. the list begins with characters like '$' and '@' which have low brightness and are mapped to pixels having darker pixel values. Towards the end of the list we have characters like '.' and ' ' which are mapped to pixels having lower pixel values. <br/>
Character map <br/>
![cmp](https://user-images.githubusercontent.com/76247110/174477858-5e77b52c-87ac-4105-99b0-c57b03a819e7.PNG) <br/>
To assign the ASCII characters to the pixels in the original image, we slice the original image into cells and take average of all the pixel values of the cell.This average value will be between 0 and 255. We then scale this average down to the length of our character map, which is 70 , and assign the corresponding character to the cell. By this method we assign all the cells characters. Now we need to assign colors to these characters. Again we take average of all the pixel values in the cell to get a tuple (x, y, z) where x, y and z are between 0 and 255. Now this tuple corresponds to an RGB color, and we assign this color to the character in the cell.<br/>
#### Internal working of ASCII video generator:
For the ASCII video generator, we generate the various frames that the video is composed of, using cv2 library in python. Then we generate the ASCII art for each of these frames, simultaneously, i.e. the ASCII art is generated as soon as we get the frame from the video. We then store all of these ASCII art converted frames in a folder. After this we merge all the images in the folder to form one video ,again using cv2 library in python. 
