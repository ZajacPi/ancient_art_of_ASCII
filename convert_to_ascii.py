import cv2
import numpy as np

Im = cv2.imread('ascii-pineapple.jpg')
Im = cv2.imread('hieroglyphics.jpeg')
Im = cv2.imread('neo.jpge')

#adjust for better quality
new_width = 600  
aspect_ratio = Im.shape[0] / Im.shape[1]
new_height = int(new_width * aspect_ratio)
pixel_matrix = cv2.resize(Im, (new_width, new_height))

X = pixel_matrix.shape[0]
Y = pixel_matrix.shape[1]

brightness_matrix = np.empty((X, Y))

for x in range(len(pixel_matrix)):
    for y in range(len(pixel_matrix[x])):
        pixel = pixel_matrix[x][y]
        # I'm going to use average
        # this works terribly
        # brightness_matrix[x][y] = (pixel[0]+pixel[1]+pixel[2])/3

        brightness_matrix[x][y] = np.mean(pixel)

ASCII = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

#dtype here us '<U3' because it takes 3 symbols
ascii_matrix = np.empty((X, Y), dtype='<U3')
for x in range(len(brightness_matrix)):
    for y in range(len(brightness_matrix[x])):
        pixel = brightness_matrix[x][y]
        # I muliply by 3, because symbols are not displayed square, but are longer than wider, 
        # so to fix this I multiply by 3
        ascii_matrix[x][y] = ASCII[int(pixel//4)]*3

for row in ascii_matrix:
    print("".join(row))