import cv2
import argparse
import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

# Characters used for Mapping to Pixels
Character = {
    "standard": "@%#*+=-:. ",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

# Function to define font and which character list is used
def get_data(mode):
    font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 20)
    char_list = Character[mode]
    return char_list, font,

# Function to define font and which character list is used
def genAscii(fname, scale, num_cols, outfname):
    # Making Background Black or White
    bg = "black"
    #bg = "white"
    if bg=="white":
        bg_code=(255, 255, 255)
    elif bg=="black":
        bg_code=(0, 0, 0)

    # Getting the character List and Font
    char_list, font = get_data("complex")
    num_chars = len(char_list)

    # Reading Input Image
    im= cv2.imread(fname)

    # Extracting height and width from Image
    height, width, _ = im.shape

    # Defining height and width of each cell==pixel
    cell_w = width/num_cols
    cell_h = int(scale*cell_w)
    num_rows = int(height/cell_h)

    # Calculating Height and Width of the output Image
    char_w, char_h = font.getsize("A")
    out_width = char_w*num_cols
    out_height = int(char_h*scale*num_rows)


    # Making a new Image using PIL
    out_im = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_im)

    # Mapping characters for RGB
    for i in range(num_rows):
        for j in range(num_cols):
            snapshot = im[int(i*cell_h):min(int((i+1)*cell_h), height), int(j*cell_w):min(int((j+1)*cell_w), width),:]
            snapshot_avg_color = np.sum(np.sum(snapshot, axis=0), axis=0)/(cell_h*cell_w)
            snapshot_avg_color = tuple(snapshot_avg_color.astype(np.int32).tolist())
            c = char_list[min(int(np.mean(snapshot)*num_chars/255), num_chars-1)]
            draw.text((j*char_w, i*char_h), c, fill = snapshot_avg_color, font=font)



    # Inverting Image and removing excess borders
    if bg=="white":
        cropped_im = ImageOps.invert(out_im).getbbox()
    elif bg == "black":
        cropped_im = out_im.getbbox()
    # Saving the new Image
    out_im = out_im.crop(cropped_im)
    out_im.save("./out1.jpg")


# Function to create a folder containing ascii art of all frames of a video
def convert_to_frames(fname, num_cols):
    # Reading input video
    vid = cv2.VideoCapture(fname)
    try:
        # Creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
    # If not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # Defining frame number
    currentframe = 0

    while (True):

        # Reading from frame
        success, frame = vid.read()

        if success:

            # Defining names for frame and ascii art of frame
            name = './data/frame' + str(currentframe) + '.jpg'
            name2 = './data/outframe' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            #print(frame)

            # Writing the extracted frames to folder
            cv2.imwrite(name, frame)

            # Creating ascii art of frames
            genAscii(name, 2, num_cols, name2)

            # Writing ascii art of frame to folder
            im1= cv2.imread("./out1.jpg")
            cv2.imwrite(name2, im1)

            # Deleting the original frame after ascii art has been added to the folder
            try:
                os.remove(name)
            except:
                pass

            # Increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    vid.release()
    cv2.destroyAllWindows()

# Function to compile given folder of frames to a video
def convert_frames_to_video(output_file_name, fps):

    # Defining path of frames folder
    path = os.getcwd()
    data_dir = 'data'
    input_frame_path = os.path.join(path, data_dir)
    input_list = os.listdir(input_frame_path)
    
    #Defining size of frame
    frame = cv2.imread(os.path.join(input_frame_path, 'outframe0.jpg'))
    height, width, channels = frame.shape
    
    # Defining the codec.FourCC is a 4-byte code used to specify the video codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    size = (width, height)
    
    # Defining the output video writer object
    out = cv2.VideoWriter(output_file_name, fourcc, fps, size)
    num_frames = len(input_list)

    # Adding frame to video
    for i in range(num_frames):
        base_name = 'outframe'
        img_name = base_name + '{:1d}'.format(i) + '.jpg'
        img_path = os.path.join(input_frame_path, img_name)
        img = cv2.imread(img_path)
        
        # Writing out frame to video
        out.write(img)
        
    # Release all space and windows once done
    out.release()
    print("The output ascii art video is {} is saved".format(output_file_name))
    
    # Destroying the folder once output video is saved
    try:
        shutil.rmtree(data_dir)
    except:
        pass

def main():
    descStr = "This program converts a video into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add arguments for input file, output file
    # fps and number of columns in final image
    parser.add_argument('--file', dest='vidFile', required=True)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--fps', dest= 'fps', required=False)
    parser.add_argument('--num_cols', dest='num_cols', required=False)
    args = parser.parse_args()

    vidFile = args.vidFile
    outFile = 'out.mp4'
    if args.outFile:
        outFile = args.outFile
    num_cols = 600
    if args.num_cols:
        num_cols = int(args.num_cols)
    fps = 6
    if args.fps:
        fps = int(args.fps)
    convert_to_frames(vidFile, num_cols)
    convert_frames_to_video(outFile, fps)

if __name__ == '__main__':
    main()
