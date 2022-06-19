import cv2, argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont
import shutil

# Characters used for Mapping to Pixels
Character = {
    "standard": "@%#*+=-:. ",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}


def get_data(mode):
    font = ImageFont.truetype("fonts\DejaVuSansMono.ttf", size = 20)
    char_list = Character[mode]
    return char_list, font,


# Making Background Black or White

def genAscii(fname, scale, num_cols, outfname):
    bg = "black"
    #bg = "white"
    if bg=="white":
        bg_code=(255, 255, 255)
    elif bg=="black":
        bg_code=(0, 0, 0)


    # Getting the character List, Font and Scaling characters for square Pixels
    char_list, font = get_data("complex")
    num_chars = len(char_list)
    #num_cols = 275
    # Reading Input Image
    im= cv2.imread(fname)

    # Converting Color Image to Grayscale
    #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
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

    # Mapping the Characters
    # for i in range(num_rows):
    #     min_h = min(int((i+1)*cell_h), height)
    #     row_pix = int(i*cell_h)
    #     # lst = [i for i in range(5)] => We can make strings/lists/tuples in this way => lst = [0, 1, 2, 3, 4]
    #     # lst[first:last] gives us a sublist from the first index to the last index excluding the last index => lst[1:4]==[1, 2, 3]
    #     line = "".join([char_list[min(int(np.mean(im[row_pix:min_h, int(j * cell_w):min(int((j + 1) * cell_w), width)]) / 255 * num_chars), num_chars - 1)]for j in range(num_cols)]) + "\n"
    #
    #     # Draw string at a given position (x,y)
    #     draw.text((0, i*char_h), line, fill = 255-bg_code, font = font)

    #mapping characters for RGB

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

def convert_to_frames(fname, num_cols):
    vid = cv2.VideoCapture(fname)
    try:

        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0

    while (True):

        # reading from frame
        success, frame = vid.read()

        if success:
            # continue creating images until video remains
            name = './data/frame' + str(currentframe) + '.jpg'
            name2 = './data/outframe' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            #print(frame)
            # writing the extracted images
            cv2.imwrite(name, frame)
            genAscii(name, 2, num_cols, name2)
            im1= cv2.imread("./out1.jpg")
            cv2.imwrite(name2, im1)
            try:
                os.remove(name)
            except:
                pass
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    vid.release()
    cv2.destroyAllWindows()

def convert_frames_to_video(output_file_name, fps):

    path = os.getcwd()
    data_dir = 'data'
    input_frame_path = os.path.join(path, data_dir)
    input_list = os.listdir(input_frame_path)
    frame = cv2.imread(os.path.join(input_frame_path, 'outframe0.jpg'))
    height, width, channels = frame.shape
    # Define the codec.FourCC is a 4-byte code used to specify the video codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    size = (width, height)
    # Define the output video writer object
    out = cv2.VideoWriter(output_file_name, fourcc, fps, size)
    num_frames = len(input_list)

    for i in range(num_frames):
        base_name = 'outframe'
        img_name = base_name + '{:1d}'.format(i) + '.jpg'
        img_path = os.path.join(input_frame_path, img_name)
        img = cv2.imread(img_path)
        out.write(img)  # Write out frame to video
    # Release everything if job is finished
    out.release()
    print("The output video is {} is saved".format(output_file_name))
    try:
        shutil.rmtree(data_dir)
    except:
        pass

def main():
    descStr = "This program converts a video into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
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