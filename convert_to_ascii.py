import cv2
import numpy as np
from colorama import Fore, Style
import os

#loading images like this is very ineffective, I would prefer if it opened a folder automatically
# Im = cv2.imread('hieroglyphics.jpg')
# Im = cv2.imread('neo.jpeg')
# Im = cv2.imread('tatras.JPG')

# I determine the path of the folder (if you cloned the repo it is different than mine, so I dont hard code it)
# You can throw the images You want to convert there
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = 'images'  
folder_path = os.path.join(script_dir, folder_name)

# then, list all files in the folder
files = os.listdir(folder_path)
image_extensions = ['.jpg', '.jpeg', '.png']
image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]

if not image_files:
    raise ValueError("The image folder is empty!")

#default settings
new_width=500
invert = 'n'
color = 'n'

#User interface
print(f"[a] Advanced options")
print(f"[ENTER] Run default")
i = input("Option: ")

if i == '':
    print("Running on default options")
elif i == 'a':
    new_width = int(input(f"Resize width (default is 500): "))
    invert = input("Invert the image [y/n]: ")
    color = input("Change color [y/n]: ")
    if color == 'y':
        color = input("[r/g/b]: ")
else:
    print("Wrong command, running default")

print("Choose the image you want to convert to ASCII:")
for i, image_name in enumerate(image_files):
    print(f"[{i+1}] {image_name}")
i = int(input("Image nr: "))

if i>len(image_files) or i < 0:
    raise ValueError("Wrong image number")



# Load the first image from the list
image_path = os.path.join(folder_path, image_files[i-1])
Im = cv2.imread(image_path)

#adjust size for better quality
def resize_image(new_width):
    aspect_ratio = Im.shape[0] / Im.shape[1]
    new_height = int(new_width * aspect_ratio)
    return cv2.resize(Im, (new_width, new_height))

pixel_matrix = resize_image(new_width)

X = pixel_matrix.shape[0]
Y = pixel_matrix.shape[1]

brightness_matrix = np.empty((X, Y))

for x in range(len(pixel_matrix)):
    for y in range(len(pixel_matrix[x])):
        pixel = pixel_matrix[x][y]
        # I'm going to use average
        # this works terribly
        # brightness_matrix[x][y] = (pixel[0]+pixel[1]+pixel[2])//3

        brightness_matrix[x][y] = np.mean(pixel)

ASCII = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
n = len(ASCII)
#dtype here us '<U3' because it takes 3 symbols
ascii_matrix = np.empty((X, Y), dtype='<U3')
inversed_ascii_matrix = np.empty((X, Y), dtype='<U3')
for x in range(len(brightness_matrix)):
    for y in range(len(brightness_matrix[x])):
        pixel = brightness_matrix[x][y]
        # because symbols are not displayed square, but are longer than wider, 
        # so to fix this I multiply by 2
        if invert == 'y':
                inversed_ascii_matrix[x][y] = ASCII[n-(int(pixel//4))-1]*2
        else:
            ascii_matrix[x][y] = ASCII[int(pixel//4)]*2

if invert == 'y':
    ascii_matrix = inversed_ascii_matrix

for row in ascii_matrix:
    if color == 'n':
        print("".join(row))
    else:
        #lets try it in color! Im gonna use the colorama module
        if color == 'r':
            print(Fore.RED + "".join(row))
        if color == 'g':
            print(Fore.GREEN + "".join(row))
        if color == 'b':
            print(Fore.BLUE + "".join(row))

print(Style.RESET_ALL)
