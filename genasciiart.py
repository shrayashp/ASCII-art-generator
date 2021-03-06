import cv2
import argparse
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

# Function to create an ascii image from image
def genAscii(fname, scale, num_cols, outfname):
    # Making Background Black or White
    bg = "black"
    #bg = "white"
    if bg=="white":
        bg_code=(255, 255, 255)
    elif bg=="black":
        bg_code=(0, 0, 0)


    # Getting the character List, Font and Scaling characters for square Pixels
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
    out_im.save(outfname)

def main():
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add arguments for input file, output file
    # scale and number of columns in final image
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--num_cols', dest='num_cols', required=False)
    args = parser.parse_args()

    imgFile = args.imgFile
    outFile = 'out.jpg'
    if args.outFile:
        outFile = args.outFile
    scale = 2
    if args.scale:
        scale = float(args.scale)
    num_cols = 200
    if args.num_cols:
        num_cols = int(args.num_cols)
    print('generating ASCII art...')
    genAscii(imgFile, scale, num_cols, outFile)

if __name__ == '__main__':
    main()
